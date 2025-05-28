from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer

from ekiladesign.permissions import IsConfirmedWebSocket
from radio.models import Radio
from radio.serializers import RadioCreateOrUpdateSerializer
from radio.serializers import WebSocketRadioSerializer


class RadioConsumer(GenericAsyncAPIConsumer):
    permission_classes = [IsConfirmedWebSocket]

    def get_queryset(self, **kwargs):
        return Radio.objects.filter(user=self.user)

    @model_observer(Radio)
    async def radio_activity(
        self, message, observer=None, subscribing_ids=[], **kwargs
    ):
        await self.send_json(message)

    @radio_activity.serializer
    def radio_activity(self, instance: Radio, action, **kwargs):
        data = {
            "radio": RadioCreateOrUpdateSerializer(instance).data,
            "action": action.value,
        }
        return WebSocketRadioSerializer(data).data

    @radio_activity.groups_for_signal
    def radio_activity(self, instance: Radio, **kwargs):
        yield f"radio_{instance.user.id}"

    @radio_activity.groups_for_consumer
    def radio_activity(self, instance=None, user=None, **kwargs):
        yield f"radio_{user.id}"

    @action()
    async def subscribe_to_radio_activity(self, request_id, **kwargs):
        user = self.scope["user"]
        await self.radio_activity.subscribe(request_id=request_id, user=user)
