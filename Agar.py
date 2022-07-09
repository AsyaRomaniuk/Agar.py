from tkinter import *
from random import randint, choice
from math import sqrt


class Player(object):
    def __init__(self, x, y, radius, mass, clr, oclr, tag):
        self.x, self.y = x, y
        self.mass = mass
        self.clr = clr
        self.oclr = oclr
        self.tag = tag
        # self.alive = True
        self.step = 5
        self.scaling = 4
        self.radius = radius

    def drawPlayer(self) -> None:
        canv.create_oval((self.x + self.mass, self.y + self.mass), (self.x - self.mass, self.y - self.mass),
                         fill=self.clr, outline=self.oclr, width=2, tag=self.tag)


def setLines(px, clr, scale=1) -> None:
    [canv.create_line((i * px * scale, 0), (i * px * scale, canvH * scale),
                      fill=clr, tag="line") for i in range(1, int(canvW / px))]
    [canv.create_line((0, i * px * scale), (canvW * scale, i * px * scale),
                      fill=clr, tag="line") for i in range(1, int(canvH / px))]
    canv.tag_lower("line")


def setBorder(bd, clr, scale=1) -> None:
    [canv.create_line(*line, fill=clr, width=bd, tag="line")
     for line in ((0, 0, canvW * scale, 0), (canvW * scale, 0, canvW * scale, canvH * scale),
                  (canvW * scale, canvH * scale, 0, canvH * scale), (0, canvH * scale, 0, 0))]
    canv.tag_lower("line")


def setFoodDots(k, mass) -> None:
    foodclrs = ("yellow", "red", "green", "pink", "purple", "blue", "lime", "aqua", "orange", "brown")
    for i in range(k):
        clr = choice(foodclrs)
        x, y = randint(0, canvW), randint(0, canvH)
        canv.create_oval((x + mass, y + mass), (x - mass, y - mass), fill=clr, outline=clr, tag="food")


def eatFood(foodId) -> None:
    canv.delete(foodId)
    player.mass += 5
    masstext.config(text=f"Mass: {player.mass}")
    k = sqrt((player.mass) / ((player.mass - 5)))
    player.radius *= k
    dr = 0.4 * player.scaling * player.radius
    # canv.create_rectangle(player.x + player.radius * player.scaling - dr,
    #                       player.y + player.radius * player.scaling - dr,
    #                       player.x - player.radius * player.scaling + dr,
    #                       player.y - player.radius * player.scaling + dr)
    canv.scale(player.tag, player.x, player.y, k, k)
    # player.scaling -= k-1 #!!!
    # canv.scale(ALL, 0, 0, x, x)


def isInCanvas(x, y, scale) -> bool:
    return True if all((x > 0, y > 0, x < canvW * scale, y < canvH * scale)) else False


def move() -> None:
    x, y = canv.winfo_pointerx() - canv.winfo_rootx(), canv.winfo_pointery() - canv.winfo_rooty()
    dr = 0.4 * player.scaling * player.radius
    ids = canv.find_overlapping(player.x + player.radius * player.scaling - dr,
                                player.y + player.radius * player.scaling - dr,
                                player.x - player.radius * player.scaling + dr,
                                player.y - player.radius * player.scaling + dr)
    [eatFood(i) for i in ids if
     canv.itemcget(i, "tag") not in ("player current", player.tag, "line", "line current")]
    l = sqrt(pow(canv.canvasx(x) - player.x, 2) + pow(canv.canvasy(y) - player.y, 2))
    normal = ((canv.canvasx(x) - player.x) / l, (canv.canvasy(y) - player.y) / l)
    if isInCanvas(player.x + normal[0] * player.step, player.y + normal[1] * player.step, player.scaling):
        ml = player.radius * player.scaling
        canv.move(player.tag, normal[0] * player.step * l / ml,
                  normal[1] * player.step * l / ml) if l < ml else canv.move(
            player.tag, normal[0] * player.step, normal[1] * player.step)
        player.x = (canv.coords(player.tag)[0] + canv.coords(player.tag)[2]) / 2
        player.y = (canv.coords(player.tag)[1] + canv.coords(player.tag)[3]) / 2
        canv.scan_dragto(-int(player.x) + int(W / 2), -int(player.y) + int(H / 2), 1)
    scene.after(time, move)


def transparentWindow() -> None:
    scene.attributes("-transparentcolor", "",
                     "-topmost", False, "-fullscreen", False) if not isTransparent.get() else scene.attributes(
        "-transparentcolor", "SystemButtonFace", "-topmost", True, "-fullscreen", True)


if __name__ == "__main__":
    scene = Tk()
    W, H = scene.winfo_screenwidth(), scene.winfo_screenheight()
    scene.state("zoomed")
    scene.title("Agar.py")
    canvW, canvH = 2000, 2000
    canv = Canvas(scene, width=canvW, height=canvH)
    canv.pack(fill=BOTH, expand=True)
    setLines(50, "silver")
    setBorder(3, "red")
    setFoodDots(1000, 5)
    rx, ry = randint(0, canvW), randint(0, canvH)
    player = Player(rx, ry, 10, 10, "red", "blue", "player")
    player.drawPlayer()
    canv.scale(ALL, 0, 0, player.scaling, player.scaling)
    canv.scan_dragto(-rx + int(W / 2), -ry + int(H / 2), 1)
    masstext = Label(scene, text=f"Mass: {player.mass}", font=("Arial", 20), fg="red")
    masstext.place(relx=0.03, rely=0.03)
    listcaption = Label(scene, text="Leaders list", font=("Arial", 20), fg="grey")
    listcaption.place(relx=0.8, rely=0.03)
    leaderlist = Label(scene, text="1. You", font=("Arial", 18), fg="grey40")
    leaderlist.place(relx=0.8, rely=0.1)
    isTransparent, isLines = BooleanVar(), BooleanVar()
    isLines.set(True)
    viewmenu = Menu(tearoff=False)
    viewmenu.add_checkbutton(label="Transparent window", onvalue=True, offvalue=False, variable=isTransparent,
                             command=transparentWindow)
    viewmenu.add_checkbutton(label="Lines", onvalue=True, offvalue=False, variable=isLines,
                             command=lambda: (setLines(50, "silver", player.scaling),
                                              setBorder(3, "black", player.scaling)
                                              if isLines.get() else canv.delete("line")))
    menu = Menu(scene)
    menu.add_cascade(label="View", menu=viewmenu)
    time = 15
    scene.after(time, move)
    scene.config(menu=menu)
    scene.mainloop()
