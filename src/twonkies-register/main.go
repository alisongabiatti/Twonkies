package main

import (
	// "fmt"
	"context"
	"github.com/alisongabiatti/Twonkies/src/internals/host"
	"github.com/alisongabiatti/Twonkies/src/internals/tasks"
	"github.com/labstack/echo/v4"
	"net/http"
	"encoding/json"
)

var ctx = context.Background()

// List all host
func hostList(c echo.Context) error {
	h := new(host.Host)
	h.GetHost(ctx)
	return c.String(http.StatusOK, h.GetHost(ctx))
}

// Register Host
func registerHost(c echo.Context) error {
	h := new(host.Host)
	if err := c.Bind(h); err != nil {
		return err
	}
	h.Register(ctx)
	return c.JSON(http.StatusCreated, h)
}

func getCommand(c echo.Context) error {
	// x := tasks.Attack.Parameters{
	// 	Worker : 5,
	// 	Load : "120mb",
	// 	Timer : 60,
	// }
	t := tasks.Attack{
		StressorName : "stress-ng",
		AttackName : "MemoryAttack",
		BinPath : "",
		CommandTemplate: "stress-ng -vm {{.Worker}} --vm-bytes {{.Load}} -t {{.Timer}}",
		Parameters : []tasks.AttackParameters{
			{
				Name: "worker",
				Help: "Numero de workers",
				Example: "3",
			},
			{
				Name: "load",
				Help: "Carga em MB",
				Example: "100",
			},
			{
				Name: "time",
				Help: "Tempo de duração do experimento em segundos",
				Example: "3",
			},
		},
		Status : "Create",
	}
	// t.Parameters = append(t.Parameters,tasks.AttackParameters{
	// 	Name: "teste",
	// 	Help: "help",
	// 	Example: "exemplo",
	// })
	// t.Parameters = append(t.Parameters,tasks.AttackParameters{
	// 	Name: "teste1",
	// 	Help: "help1",
	// 	Example: "exemplo1",
	// })
	// t.Command(ctx)
	json.Marshal(t)
	return c.JSON(http.StatusOK, t)
}
func main() {
	e := echo.New()
	e.GET("/hosts", hostList)
	e.GET("/tst", getCommand)
	e.POST("/host", registerHost)
	e.Logger.Fatal(e.Start(":8080"))

}
