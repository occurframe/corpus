module oracle-runner

go 1.24

require (
	github.com/robfig/cron/v3 v3.0.1
	github.com/teambition/rrule-go v1.8.2
)

replace github.com/robfig/cron/v3 => ../../engines/robfig-cron

replace github.com/teambition/rrule-go => ../../engines/rrule-go
