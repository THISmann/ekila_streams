from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer

from ekiladesign.models import Publicite
from ekiladesign.permissions import IsConfirmedWebSocket
from ekiladesign.serializers import PubliciteUpdateSerializer
from ekiladesign.serializers import WebSocketPublicitySerializer


class PublicityConsumer(GenericAsyncAPIConsumer):
    permission_classes = [IsConfirmedWebSocket]

    def get_queryset(self, **kwargs):
        return Publicite.objects.filter(user=self.user)

    @model_observer(Publicite)
    async def publicity_activity(
        self, message, observer=None, subscribing_ids=[], **kwargs
    ):
        await self.send_json(message)

    @publicity_activity.serializer
    def publicity_activity(self, instance: Publicite, action, **kwargs):
        data = {
            "publicity": PubliciteUpdateSerializer(instance).data,
            "action": action.value,
        }
        return WebSocketPublicitySerializer(data).data

    @publicity_activity.groups_for_signal
    def publicity_activity(self, instance: Publicite, **kwargs):
        yield f"publicity_{instance.user.id}"

    @publicity_activity.groups_for_consumer
    def publicity_activity(self, instance=None, user=None, **kwargs):
        yield f"publicity_{user.id}"

    @action()
    async def subscribe_to_publicity_activity(self, request_id, **kwargs):
        user = self.scope["user"]
        await self.publicity_activity.subscribe(request_id=request_id, user=user)
