package host

import (
	"reflect"
	"github.com/alisongabiatti/Twonkies/src/internals/rds"
)

type Host struct {
	Uid      string `json:"uid"`
	Hostname string `json:"hostname"`
	Machine  string `json:"machine"`
	Platform string `json:"platform"`
	Status   string `json:"status"`
}

func structToMap(item interface{}) map[string]interface{} {

	res := map[string]interface{}{}
	if item == nil {
		return res
	}
	v := reflect.TypeOf(item)
	reflectValue := reflect.ValueOf(item)
	reflectValue = reflect.Indirect(reflectValue)

	if v.Kind() == reflect.Ptr {
		v = v.Elem()
	}
	for i := 0; i < v.NumField(); i++ {
		tag := v.Field(i).Tag.Get("json")
		field := reflectValue.Field(i).Interface()
		if tag != "" && tag != "-" {
			if v.Field(i).Type.Kind() == reflect.Struct {
				res[tag] = structToMap(field)
			} else {
				res[tag] = field
			}
		}
	}
	return res
}

func (h Host) Register() {
	hostTag := "host:" + h.Uid
	host := structToMap(h)
	host["status"]="created"
	rds.RClient().HSet(rds.Ctx, hostTag, host)
}

func (h Host) Pong() {
	hostTag := "host:" + h.Uid
	rds.RClient().HSet(rds.Ctx, hostTag, "status", h.Status)
}
