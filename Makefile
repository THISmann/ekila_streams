# check_defined = \
# $(strip $(foreach 1,$1, \
# $(call __check_defined,$1,$(strip $(value 2)))))

# __check_defined = \
# $(if $(value $1),, \
# $(error Undefined $1$(if $2, ($2))))
# @:$(call check_defined, tag)
# set +e command used to exit on error (errexit)


builddocker:
	docker build -t ekilastreams-back:1.0.SNAPSHOT .

wait_db:
	python manage.py wait_for_db

migrate:
	python manage.py makemigrations && python manage.py migrate --noinput

flushdb:
	python manage.py flush -y

collectstatic:
	python manage.py collectstatic --noinput

# check for difference commit and current and update the branch
update:
	set +e
	git diff --quiet && git diff --cached --quiet
	retcode=$?
	set -e
	if [[ $retcode != 0 ]]; then
	    echo "There are uncommitted changes:"
	    git status
	    exit 1
	fi
	git pull
