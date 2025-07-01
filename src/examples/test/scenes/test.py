import pyxora
import pyxora.utils

from time import perf_counter as time

pygame = pyxora.pygame

class Test(pyxora.Scene):
    def _on_create(self):
        print(f"Scene created at {time()}")

    def _start(self):
        self.background_color = "gray"
        self.event.create("hello_world",-1)
        self.event.create("performance",1)
        self.event.create("print_delay",0)

        self.event.schedule("hello_world",1000)
        self.event.schedule("performance",1000)
        self.event.schedule("print_delay",100)

        self.rect = pyxora.Rect(self.display.get_center(),(200,200),"black")
        self.circle = pyxora.Circle(self.display.get_center(),100,"red")
        self.circle2 = pyxora.Circle((0,0),200,"blue")

        self.icon = pyxora.Image(self.assets.get("engine","images","logo"),(0,0),align="topleft")

        self.text = pyxora.Text("This is a text",self.display.get_center(),"white",align="center")

        print("Scene Start")

    def _on_keydown(self,key):
        key == "p" and self.manager.pause()
        key == "f5" and self.display.toggle_fullscreen()
        key == "r" and self.manager.restart()
        key == "`" and self.manager.reset()

    def _on_restart(self):
        print("Scene Restart")

    def _on_reset(self):
        print("Scene Reset")

    def _on_paused_keydown(self,key):
        key == "p" and self.manager.resume()

    def _on_keypressed(self,keys):
        speed = 100
        "a" in keys and self.camera.move((-speed*self.dt,0))
        "d" in keys and self.camera.move((speed*self.dt,0))
        "w" in keys and self.camera.move((0,-speed*self.dt))
        "s" in keys and self.camera.move((0,speed*self.dt))

        "right" in keys and self.circle.move((speed*self.dt,0))
        "left" in keys and self.circle.move((-speed*self.dt,0))
        "up" in keys and self.circle.move((0,-speed*self.dt))
        "down" in keys and self.circle.move((0,speed*self.dt))

        self.is_custom_event("print_delay") and print(f"[INPUT] keys{keys}")

    @pyxora.utils.event_listener("print_delay")
    def _on_paused_keypressed(self,keys):
        print(f"[PAUSED][INPUT] keys{keys}")

    def _on_mousewheel(self,wheel):
        wheel == "up" and self.camera.zoom(2)
        wheel == "down" and self.camera.zoom(-2)

    def _update(self):
        self.print_performance()
        self.rect.move((10*self.dt,0))

    def _paused_update(self):
        self.print_hello()

    def _draw(self):
        self.camera.draw_shape(self.rect,fill=10)
        self.camera.draw_shape(self.circle,fill=5)
        self.camera.draw_shape(self.circle2,fill=5)
        self.camera.draw_image(self.icon)
        self.camera.draw_text(self.text)

    @pyxora.utils.event_listener("hello_world")
    def print_hello(self):
        counter = self.event.get("hello_world").calls
        print("[EVENT] Hello World",counter)

    @pyxora.utils.event_listener("performance")
    def print_performance(self):
        print(f"[EVENT] runtime: {int(self.runtime)}s, fps: {round(self.fps)}, dt: {self.dt}")
