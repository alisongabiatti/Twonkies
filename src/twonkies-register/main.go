package main

import (
	// "fmt"
	"net/http"

	"github.com/alisongabiatti/Twonkies/src/internals/host"
	"github.com/labstack/echo/v4"
)

func hostList(c echo.Context) error {
	return c.String(http.StatusOK, "Hello, World!")
}
func registerHost(c echo.Context) error {
	h := new(host.Host)
	if err := c.Bind(h); err != nil {
		return err
	}
	h.Register()
	return c.JSON(http.StatusCreated, h)
}
func pongHost(c echo.Context) error {
	h := new(host.Host)
	if err := c.Bind(h); err != nil {
		return err
	}
	h.Pong()
	return c.JSON(http.StatusCreated, h)
}
func main() {
	e := echo.New()
	e.GET("/hosts", hostList)
	e.POST("/host", registerHost)
	e.POST("/host/pong", pongHost)
	e.Logger.Fatal(e.Start(":8080"))

}
