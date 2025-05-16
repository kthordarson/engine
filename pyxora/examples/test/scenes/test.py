import pyxora
import pyxora.utils

from time import perf_counter as time

pygame = pyxora.pygame
    
class Test(pyxora.Scene):
    def _on_create(self):
        self.rect = pyxora.Rect(self.Display.get_center(),(200,200),"black")
        self.circle = pyxora.Circle(self.Display.get_center(),100,"red")
        self.circle2 = pyxora.Circle((0,0),200,"blue")

        ms = round(self.get_delay() * 1000)
        print(f"Scene created with : {ms}ms delay")

    def _start(self):
        self.background_color = "gray"
        self.Event.create("hello_world",-1)
        self.Event.create("performance",1)
        self.Event.create("print_delay",0)

        self.Event.schedule("hello_world",1000)
        self.Event.schedule("performance",1000)
        self.Event.schedule("print_delay",100)
        print(f"Scene Start")

    def _on_keydown(self,key):
        key == "p" and self.Manager.pause()
        key == "f5" and self.Display.toggle_fullscreen()

    def _on_paused_keydown(self,key):
        key == "p" and self.Manager.resume()

    def _on_keypressed(self,keys):
        speed = 100
        "a" in keys and self.circle.move((-speed*self.dt,0))
        "d" in keys and self.circle.move((speed*self.dt,0))
        "w" in keys and self.circle.move((0,-speed*self.dt))
        "s" in keys and self.circle.move((0,speed*self.dt))

        self.is_custom_event("print_delay") and print(f"[INPUT] keys{keys}")

    @pyxora.utils.event_listener("print_delay")
    def _on_paused_keypressed(self,keys):
        print(f"[PAUSED][INPUT] keys{keys}")

    @pyxora.utils.event_listener("print_delay")
    def _on_mousewheel(self,wheel):
        print(f"[INPUT] wheel:{wheel}")

    def _update(self):
        self.print_performance()
        self.rect.move((10*self.dt,0))

    def _paused_update(self):
        self.print_hello()

    def _draw(self):
        self.Display.draw_shape(self.rect,fill=10)
        self.Display.draw_shape(self.circle,fill=5)
        self.Display.draw_shape(self.circle2,fill=5)

    @pyxora.utils.event_listener("hello_world")
    def print_hello(self):
        counter = self.Event.get("hello_world").calls
        print("[EVENT] Hello World",counter)

    @pyxora.utils.event_listener("performance")
    def print_performance(self):
        print(f"[EVENT] runtime: {int(self.runtime)}s, fps: {round(self.fps)}, dt: {self.dt}")

    def get_delay(self):
        return time() - self._global_start_time