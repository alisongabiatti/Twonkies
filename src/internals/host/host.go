package host

import (
	"context"
	"encoding/json"

	"github.com/alisongabiatti/Twonkies/src/internals/rds"
)

type Host struct {
	Uid      string `json:"uid"`
	Hostname string `json:"hostname"`
	Machine  string `json:"machine"`
	Platform string `json:"platform"`
	Status   string `json:"status"`
}

func (h Host) Register(ctx context.Context) {

	host, err := json.Marshal(h)
	if err != nil {
		print(err)
	}
	rds.Redis.HSet(ctx, "host", h.Uid, string(host))

}

// func (h Host) Pong(ctx context.Context) {
// 	hostTag := "host:" + h.Uid
// 	rds.Redis.Set(ctx, hostTag, "status", h.Status)
// }
