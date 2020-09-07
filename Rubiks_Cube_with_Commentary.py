# These are the modules used for running the program:

# The Random module randomly generates numbers and makes choices. This allows the program to scramble the cube and
# decide what side to start on when solving it.
import random

# The Tkinter module opens windows and places shapes, text, and colors on them. All of the graphics run through Tkinter.
import tkinter as tk



# principal() acts as the program's main function, and it is called at the very end of the script after everything else
# is defined. It creates a hexadecimal numbering system, runs the class, and keeps the window open until you close it.
# Almost all variables and functions are named in Spanish, mainly so that I could become more familiar with Spanish
# vocabulary as I coded this. However, I would not recommend depending on a dictionary, since half the words are inside
# jokes only I understand.
def principal():
    global hexadecimal
    hexadecimal = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    programa = Ir()
    programa.ventana.mainloop()


# Rounds decimals to whole numbers
def redondear(numero):
    if abs(numero - int(numero)) < 0.5:
        repuesta = int(numero)
    elif numero > 0:
        repuesta = int(numero)+1
    else:
        repuesta = int(numero)-1
    return repuesta


# Finds the factorial of a number, which is used in the sine and cosine functions that follow
def factorial(numero):
    repuesta = 1
    for cero in range(2, numero+1):
        repuesta *= cero
    return repuesta


# Finds the sine of a number using a Taylor polynomial
def sen(numero):
    numero = numero % 6.283185307179586
    repuesta = numero
    potencia = 3
    coef = -1
    while potencia < 60:
        repuesta += coef * numero ** potencia / factorial(potencia)
        potencia += 2
        coef *= -1
    return repuesta


# Finds the cosine of a number using a Taylor polynomial
def cos(numero):
    numero = numero % 6.283185307179586
    repuesta = 1
    potencia = 2
    coef = -1
    while potencia < 60:
        repuesta += coef * numero ** potencia / factorial(potencia)
        potencia += 2
        coef *= -1
    return repuesta


# This function multiplies 3 quaternions together. Quaternions are essentially 4-dimensional complex numbers that do a
# fantastic job portraying 3-dimensional objects. Additionally, multiplying specific quaternions can imitate 3D
# rotation. To learn more, I highly recommend 3Blue1Brown's content on YouTube. Just know that this tiny function is the
# crux of anything involving rotation.
def cuaternion(c, punto, c_1):
    producto = [c[0]*punto[0] - c[1]*punto[1] - c[2]*punto[2] - c[3]*punto[3],
                c[0]*punto[1] + c[1]*punto[0] + c[2]*punto[3] - c[3]*punto[2],
                c[0]*punto[2] + c[2]*punto[0] - c[1]*punto[3] + c[3]*punto[1],
                c[0]*punto[3] + c[3]*punto[0] + c[1]*punto[2] - c[2]*punto[1]]
    repuesta = [0, producto[0]*c_1[1] + producto[1]*c_1[0] + producto[2]*c_1[3] - producto[3]*c_1[2],
                producto[0]*c_1[2] + producto[2]*c_1[0] - producto[1]*c_1[3] + producto[3]*c_1[1],
                producto[0]*c_1[3] + producto[3]*c_1[0] + producto[1]*c_1[2] - producto[2]*c_1[1]]
    return repuesta


# This function changes the color of a square sticker based on its direction. It is responsible for the animated
# "shadow" effect.
def luz(color, vector):
    i = 0.3922322702763681
    j = 0.5883484054145521
    k = 0.7071067811865476
    numero = redondear((i * vector[1] - j * vector[2] - k * vector[3]) * 63)
    r = max(hexadecimal.index(color[1]) * 16 + hexadecimal.index(color[2]) + numero, 0)
    v = max(hexadecimal.index(color[3]) * 16 + hexadecimal.index(color[4]) + numero, 0)
    a = max(hexadecimal.index(color[5]) * 16 + hexadecimal.index(color[6]) + numero, 0)
    r = hexadecimal[r // 16] + hexadecimal[r % 16]
    v = hexadecimal[v // 16] + hexadecimal[v % 16]
    a = hexadecimal[a // 16] + hexadecimal[a % 16]
    return "#"+r+v+a



# Ir() is a class that creates the cube and allows you to interact with it.
class Ir():

    # This is the first function in the class, and it sets everything up. It creates the cube, the background, and the
    # interface. The functions self.Sistema(), self.Primero_Boton(), and self.Boton() are found at the end, and they can
    # show you more of what exactly is being set up.
    def __init__(self):
        self.Sistema()
        self.ventana = tk.Tk()
        self.ventana.protocol("WM_DELETE_WINDOW", self.Terminar)
        self.ventana.configure(bg="#83D9D9", width=512, height=640)
        self.ventana.title("The Cube of Rubik")
        self.estuche = tk.Frame(self.ventana, bg="#83D9D9", height=512, width=512)
        self.otro_lugar = tk.Frame(self.ventana, bg="#000000")
        self.marco = tk.Frame(self.otro_lugar, bg="#00A8C0", height=127, width=508)
        self.espacio = tk.Canvas(self.estuche, bg="#83D9D9", borderwidth=0, highlightthickness=0, height=512, width=512)
        self.estuche.grid(row=0, column=0)
        self.otro_lugar.grid(row=1, column=0, sticky="WE")
        self.marco.grid(padx=2, pady=2)
        self.espacio.pack()
        equis = int(self.ventana.winfo_screenwidth() / 2 - self.ventana.winfo_reqwidth() / 2)
        igriega = int(64 * self.ventana.winfo_screenheight() / 900)
        self.ventana.geometry("+{}+{}".format(equis, igriega))
        self.Girar(-0.3926990816987241, 0, 1)
        self.Girar(0.2855993321445267, 1, 0)
        self.Crear()
        self.Primero_Boton()
        self.Boton()



    #           ORGANIZATION AND ANIMATION

    # This function allows multiple animations to happen at once, such as rotating a side while orienting the entire
    # cube. It also paces the program and prevents it from crashing.
    def Cambiar(self):
        declaracion = True
        if self.rg != None:
            self.Girar(self.rg[0], self.rg[1], self.rg[2])
            self.rg = None
            declaracion = False
        if self.ra != None:
            if self.tiempo != 0 and self.muy_pequena:
                self.Animar(self.ra[0], self.ra[1])
            else:
                self.Girar_lado(self.ra[0], self.ra[1])
                self.ra = None
                if not self.muy_pequena:
                    self.muy_pequena = True
            declaracion = False
        if declaracion:
            self.serie = True
        elif self.abierta:
            self.Crear()
            if self.abierta:
                self.ventana.after(0, self.Cambiar)


    # This uses information about the cube to create a series of shapes. Because it is so precise, these shapes come
    # together to look like a 3D cube. The shapes must be created in order from farthest to closest to yield a cohesive
    # image.
    def Crear(self):
        self.cuadro = [[self.vertice[0], self.vertice[2], self.vertice[6], self.vertice[4]],
                       [self.vertice[0], self.vertice[1], self.vertice[3], self.vertice[2]],
                       [self.vertice[0], self.vertice[1], self.vertice[5], self.vertice[4]],
                       [self.vertice[1], self.vertice[3], self.vertice[7], self.vertice[5]],
                       [self.vertice[4], self.vertice[5], self.vertice[7], self.vertice[6]],
                       [self.vertice[2], self.vertice[3], self.vertice[7], self.vertice[6]]]
        if True in self.transicion:
            self.tercio = [[self.v_temp[0], self.v_temp[2], self.v_temp[6], self.v_temp[4]],
                           [self.v_temp[0], self.v_temp[1], self.v_temp[3], self.v_temp[2]],
                           [self.v_temp[0], self.v_temp[1], self.v_temp[5], self.v_temp[4]],
                           [self.v_temp[1], self.v_temp[3], self.v_temp[7], self.v_temp[5]],
                           [self.v_temp[4], self.v_temp[5], self.v_temp[7], self.v_temp[6]],
                           [self.v_temp[2], self.v_temp[3], self.v_temp[7], self.v_temp[6]]]
            cual = self.transicion.index(True)
            for cero in range(6):
                for uno in range(4):
                    if self.vertice[self.caras[cual][uno]] in self.cuadro[cero]:
                        dos_temp = self.cuadro[cero].index(self.vertice[self.caras[cual][uno]])
                        self.cuadro[cero][dos_temp] = self.filo[self.bloque[cual][uno]]
            for cero in range(6):
                for uno in range(4):
                    if self.v_temp[self.caras[(cual+3)%6][uno]] in self.tercio[cero]:
                        dos_temp = self.tercio[cero].index(self.v_temp[self.caras[(cual+3)%6][uno]])
                        self.tercio[cero][dos_temp] = self.f_temp[self.bloque[cual][uno]]
            self.Ordenar(cual)
            self.espacio.delete("all")
            for cero in self.todos:
                if cero[0] == 0:
                    lista = []
                    for uno in self.cuadro[cero[1]]:
                        lista.append(256 + redondear(720 * uno[1] / (uno[3] + 4)))
                        lista.append(256 + redondear(720 * uno[2] / (uno[3] + 4)))
                    self.espacio.create_polygon(lista, fill="#000000", outline="#000000", width=1)
                    for uno in range(9):
                        declaracion = True
                        if cero[1] == cual:
                            declaracion = False
                        elif cero[1] in self.al_lado_des[cual]:
                            terma = self.al_lado_des[cual].index(cero[1])
                            if uno in self.de_al_lado_des[cual][terma]:
                                declaracion = False
                        if declaracion:
                            fracciones = self.ubicaciones[cero[1]][uno]
                            lista = []
                            for dos in fracciones:
                                lista.append(256 + redondear(720 * dos[0] / (dos[2] + 4)))
                                lista.append(256 + redondear(720 * dos[1] / (dos[2] + 4)))
                            if self.contraste:
                                nuevo_color = luz(self.conversion[self.cubo_de_roobit[cero[1]][uno]],
                                                                  self.vectores[cero[1]])
                            else:
                                nuevo_color = self.conversion[self.cubo_de_roobit[cero[1]][uno]]
                            self.espacio.create_polygon(lista, fill=nuevo_color, width=0)
                else:
                    lista = []
                    for uno in self.tercio[cero[1]]:
                        lista.append(256 + redondear(720 * uno[1] / (uno[3] + 4)))
                        lista.append(256 + redondear(720 * uno[2] / (uno[3] + 4)))
                    self.espacio.create_polygon(lista, fill="#000000", outline="#000000", width=1)
                    for uno in range(9):
                        declaracion = False
                        if cero[1] == cual:
                            declaracion = True
                        elif cero[1] in self.al_lado_des[cual]:
                            terma = self.al_lado_des[cual].index(cero[1])
                            if uno in self.de_al_lado_des[cual][terma]:
                                declaracion = True
                        if declaracion:
                            fracciones = self.ubi_temp[cero[1]][uno]
                            lista = []
                            for dos in fracciones:
                                lista.append(256 + redondear(720 * dos[0] / (dos[2] + 4)))
                                lista.append(256 + redondear(720 * dos[1] / (dos[2] + 4)))
                            if self.contraste:
                                if cero[1] == cual:
                                    nuevo_color = luz(self.conversion[self.cubo_de_roobit[cero[1]][uno]],
                                                  self.vectores[cual])
                                else:
                                    nuevo_color = luz(self.conversion[self.cubo_de_roobit[cero[1]][uno]],
                                                      self.vec_temp[self.al_lado_des[cual].index(cero[1])])
                            else:
                                nuevo_color = self.conversion[self.cubo_de_roobit[cero[1]][uno]]
                            self.espacio.create_polygon(lista, fill=nuevo_color, width=0)
        else:
            self.Ordenar(None)
            self.espacio.delete("all")
            for cero in self.verdad:
                lista = []
                for uno in self.cuadro[cero]:
                    lista.append(256 + redondear(720 * uno[1] / (uno[3] + 4)))
                    lista.append(256 + redondear(720 * uno[2] / (uno[3] + 4)))
                self.espacio.create_polygon(lista, fill="#000000", outline="#000000", width=1)
                for uno in range(9):
                    fracciones = self.ubicaciones[cero][uno]
                    lista = []
                    for dos in fracciones:
                        lista.append(256 + redondear(720 * dos[0] / (dos[2] + 4)))
                        lista.append(256 + redondear(720 * dos[1] / (dos[2] + 4)))
                    if self.contraste:
                        nuevo_color = luz(self.conversion[self.cubo_de_roobit[cero][uno]], self.vectores[cero])
                    else:
                        nuevo_color = self.conversion[self.cubo_de_roobit[cero][uno]]
                    self.espacio.create_polygon(lista, fill=nuevo_color, width=0)
        if self.abierta:
            self.ventana.update()
        if self.regla == 3:
            self.regla = 1


    # Determines which sides of the cube are closest and which are farthest. This information is used by self.Crear(),
    # self.Ay_caramba(), and other functions.
    def Ordenar(self, cual):
        lista = []
        for cero in range(6):
            numero = 0
            for uno in self.cuadro[cero]:
                numero += uno[3]
            if len(lista) == 0 or lista[len(lista)-1][1] <= numero:
                lista.append([cero, numero])
            else:
                var = 0
                while lista[var][1] < numero:
                    var += 1
                lista.insert(var, [cero, numero])
        self.verdad = [lista[2][0], lista[1][0], lista[0][0]]
        if cual != None:
            lista_grande = []
            for cero in range(6):
                numero = 0
                for uno in self.tercio[cero]:
                    numero += uno[3]
                if len(lista_grande) == 0 or lista_grande[len(lista_grande) - 1][1] <= numero:
                    lista_grande.append([cero, numero])
                else:
                    var = 0
                    while lista_grande[var][1] < numero:
                        var += 1
                    lista_grande.insert(var, [cero, numero])
            if self.vectores[cual][3] > -0.023841473169660888:
                self.todos = [[1, lista_grande[2][0]], [1, lista_grande[1][0]], [1, lista_grande[0][0]],
                              [0, lista[2][0]], [0, lista[1][0]], [0, lista[0][0]]]
            else:
                self.todos = [[0, lista[2][0]], [0, lista[1][0]], [0, lista[0][0]],
                              [1, lista_grande[2][0]], [1, lista_grande[1][0]], [1, lista_grande[0][0]]]
            if not [0, cual] in self.todos:
                self.todos.insert(0, [0, cual])
            porque = (cual+3)%6
            if not [1, porque] in self.todos:
                self.todos.insert(0, [1, porque])


    # Determines which side is above and which is to the left of the closest side. This is used for manual controls (key
    # presses).
    def Ay_caramba(self):
        proximo = self.verdad[2]
        lista = []
        for cero in range(4):
            numero = self.cuadro[proximo][cero][2]
            if len(lista) == 0 or lista[len(lista) - 1][1] <= numero:
                lista.append([cero, numero])
            else:
                var = 0
                while lista[var][1] < numero:
                    var += 1
                lista.insert(var, [cero, numero])
        punto_a = self.caras[self.verdad[2]][lista[0][0]]
        punto_b = self.caras[self.verdad[2]][lista[1][0]]
        cara = 0
        if cara == proximo:
            cara+=1
        while not (punto_a in self.caras[cara] and punto_b in self.caras[cara]):
            cara+=1
            if cara == proximo:
                cara += 1
        self.caramba = cara
        self.ay = self.al_lado_des[proximo][(self.al_lado_des[proximo].index(cara)-1)%4]


    # Ensures no errors occur when closing the window
    def Terminar(self):
        if not self.abierta:
            self.ventana.destroy()
        else:
            self.abierta = False
            self.ventana.after(17, self.Terminar)



    #           ROTATION

    # This function rotates every point on the cube using quaternions. It orients it in certain directions but does not
    # rotate individual sides.
    def Girar(self, angulo, v, h):
        r_del_r = [cos(angulo/2), v * sen(angulo/2), h * sen(angulo/2), 0]
        reciproco = [cos(-angulo/2), v * sen(-angulo/2), h * sen(-angulo/2), 0]
        for cero in range(8):
            self.vertice[cero] = cuaternion(r_del_r, self.vertice[cero], reciproco)
        for cero in range(24):
            lista = self.filo[cero]
            lejos = (lista[1]**2 + lista[2]**2 + lista[3]**2)**0.5
            numero = cuaternion(r_del_r, [0, lista[1] / lejos, lista[2] / lejos, lista[3] / lejos], reciproco)
            self.filo[cero] = [0, lejos * numero[1], lejos * numero[2], lejos * numero[3]]
        for cero in range(6):
            for uno in range(9):
                for dos in range(4):
                    lista = self.ubicaciones[cero][uno][dos]
                    lejos = (lista[0]**2 + lista[1]**2 + lista[2]**2)**0.5
                    numero = cuaternion(r_del_r, [0, lista[0] / lejos, lista[1] / lejos, lista[2] / lejos], reciproco)
                    self.ubicaciones[cero][uno][dos] = [lejos * numero[1] , lejos * numero[2], lejos * numero[3]]
        for cero in range(6):
            self.vectores[cero] = cuaternion(r_del_r, self.vectores[cero], reciproco)
        if True in self.transicion:
            for cero in range(8):
                self.v_temp[cero] = cuaternion(r_del_r, self.v_temp[cero], reciproco)
            for cero in range(24):
                lista = self.f_temp[cero]
                lejos = (lista[1] ** 2 + lista[2] ** 2 + lista[3] ** 2) ** 0.5
                numero = cuaternion(r_del_r, [0, lista[1] / lejos, lista[2] / lejos, lista[3] / lejos], reciproco)
                self.f_temp[cero] = [0, lejos * numero[1], lejos * numero[2], lejos * numero[3]]
            for cero in range(6):
                if self.ubi_temp[cero] != None:
                    for uno in range(9):
                        for dos in range(4):
                            lista = self.ubi_temp[cero][uno][dos]
                            lejos = (lista[0] ** 2 + lista[1] ** 2 + lista[2] ** 2) ** 0.5
                            numero = cuaternion(r_del_r, [0, lista[0]/lejos, lista[1]/lejos, lista[2]/lejos], reciproco)
                            self.ubi_temp[cero][uno][dos] = [lejos * numero[1], lejos * numero[2], lejos * numero[3]]
            for cero in range(4):
                self.vec_temp[cero] = cuaternion(r_del_r, self.vec_temp[cero], reciproco)


    # This function rotates the sides on an informational level, so that the computer knows how the cube should look.
    def Girar_lado(self, cara, coso):
        nueva = [self.cubo_de_roobit[0][:], self.cubo_de_roobit[1][:], self.cubo_de_roobit[2][:],
                 self.cubo_de_roobit[3][:], self.cubo_de_roobit[4][:], self.cubo_de_roobit[5][:]]
        declaracion = (cara == 0) or (cara == 1) or (cara == 5)
        if (coso and declaracion) or not (coso or declaracion):
            self.cubo_de_roobit[cara][0] = nueva[cara][6]
            self.cubo_de_roobit[cara][1] = nueva[cara][3]
            self.cubo_de_roobit[cara][2] = nueva[cara][0]
            self.cubo_de_roobit[cara][3] = nueva[cara][7]
            self.cubo_de_roobit[cara][5] = nueva[cara][1]
            self.cubo_de_roobit[cara][6] = nueva[cara][8]
            self.cubo_de_roobit[cara][7] = nueva[cara][5]
            self.cubo_de_roobit[cara][8] = nueva[cara][2]
        else:
            self.cubo_de_roobit[cara][6] = nueva[cara][0]
            self.cubo_de_roobit[cara][3] = nueva[cara][1]
            self.cubo_de_roobit[cara][0] = nueva[cara][2]
            self.cubo_de_roobit[cara][7] = nueva[cara][3]
            self.cubo_de_roobit[cara][1] = nueva[cara][5]
            self.cubo_de_roobit[cara][8] = nueva[cara][6]
            self.cubo_de_roobit[cara][5] = nueva[cara][7]
            self.cubo_de_roobit[cara][2] = nueva[cara][8]
        ciclo = self.al_lado_des[cara]
        cuadros = self.de_al_lado_des[cara]
        if coso:
            for cero in range(3):
                self.cubo_de_roobit[ciclo[0]][cuadros[0][cero]] = nueva[ciclo[3]][cuadros[3][cero]]
                self.cubo_de_roobit[ciclo[1]][cuadros[1][cero]] = nueva[ciclo[0]][cuadros[0][cero]]
                self.cubo_de_roobit[ciclo[2]][cuadros[2][cero]] = nueva[ciclo[1]][cuadros[1][cero]]
                self.cubo_de_roobit[ciclo[3]][cuadros[3][cero]] = nueva[ciclo[2]][cuadros[2][cero]]
        else:
            for cero in range(3):
                self.cubo_de_roobit[ciclo[0]][cuadros[0][cero]] = nueva[ciclo[1]][cuadros[1][cero]]
                self.cubo_de_roobit[ciclo[1]][cuadros[1][cero]] = nueva[ciclo[2]][cuadros[2][cero]]
                self.cubo_de_roobit[ciclo[2]][cuadros[2][cero]] = nueva[ciclo[3]][cuadros[3][cero]]
                self.cubo_de_roobit[ciclo[3]][cuadros[3][cero]] = nueva[ciclo[0]][cuadros[0][cero]]
        if self.regla == 2:
            self.regla = 3


    # This function provides the information necessary for animating side rotations. It also uses quaternion
    # multiplication for this purpose. Note that this function is never used during a "Quick Solve".
    def Animar(self, cara, coso):
        if self.circunferencia == 0:
            self.v_temp = []
            for cero in self.vertice:
                self.v_temp.append(cero[:])
            self.f_temp = []
            for cero in self.filo:
                self.f_temp.append(cero[:])
            self.ubi_temp = []
            for cero in range(6):
                if cero != (cara + 3) % 6:
                    self.ubi_temp.append([])
                    for uno in range(9):
                        self.ubi_temp[cero].append([])
                        for dos in range(4):
                            self.ubi_temp[cero][uno].append(self.ubicaciones[cero][uno][dos][:])
                else:
                    self.ubi_temp.append(None)
            self.vec_temp = []
            for cero in self.al_lado_des[cara]:
                self.vec_temp.append(self.vectores[cero][:])
            self.transicion[cara] = True
        if self.circunferencia < 16:
            if coso:
                angulo = -0.09817477042468103
            else:
                angulo = 0.09817477042468103
            v = self.vectores[cara][1]
            h = self.vectores[cara][2]
            a = self.vectores[cara][3]
            r_del_r = [cos(angulo/2), v * sen(angulo/2), h * sen(angulo/2), a * sen(angulo/2)]
            reciproco = [cos(-angulo/2), v * sen(-angulo/2), h * sen(-angulo/2), a * sen(-angulo/2)]
            for cero in self.caras[cara]:
                self.v_temp[cero] = cuaternion(r_del_r, self.v_temp[cero], reciproco)
            for cero in self.bloque[cara]:
                lista = self.f_temp[cero]
                lejos = ((lista[1])**2 + (lista[2])**2 + (lista[3])**2)**0.5
                numero = cuaternion(r_del_r, [0, (lista[1]) / lejos, (lista[2]) / lejos, (lista[3]) / lejos], reciproco)
                self.f_temp[cero] = [0, lejos * numero[1], lejos * numero[2], lejos * numero[3]]
            for cero in range(6):
                if self.ubi_temp[cero] != None:
                    for uno in range(9):
                        for dos in range(4):
                            lista = self.ubi_temp[cero][uno][dos]
                            lejos = (lista[0] ** 2 + lista[1] ** 2 + lista[2] ** 2) ** 0.5
                            numero = cuaternion(r_del_r, [0, lista[0]/lejos, lista[1]/lejos, lista[2]/lejos], reciproco)
                            self.ubi_temp[cero][uno][dos] = [lejos * numero[1], lejos * numero[2], lejos * numero[3]]
            for cero in range(4):
                self.vec_temp[cero] = cuaternion(r_del_r, self.vec_temp[cero], reciproco)
            self.circunferencia += 1
        else:
            self.transicion = [False] * 6
            self.circunferencia = 0
            self.Girar_lado(cara, coso)
            self.ra = None



    #           ARTIFICIAL INTELLIGENCE / COMPUTER SOLVING

    # When a side is rotated, the AI has to be temporarily interrupted. This function checks the status of the rotation
    # frequently. When the rotation is complete, it returns to whatever step the AI was on.
    def Sala_de_espera(self):
        if self.regla == 0 and self.abierta:
            if self.ra == None:
                func = self.volver
                numero = self.tiempo
                self.volver = None
            else:
                func = self.Sala_de_espera
                if self.tiempo == 0:
                    numero = 2
                else:
                    numero = 16
            if self.abierta:
                self.ventana.after(numero, func)


    # Algorithms can be stored in the list, self.recordar. This function executes those algorithms then returns to
    # whatever step the AI was on.
    def Algoritmo(self):
        if self.regla == 0:
            if len(self.recordar) > 1:
                termino_1, termino_2 = self.recordar[0]
                self.ra = (termino_1, termino_2)
                if self.recordar != []:
                    self.recordar.pop(0)
                self.volver = self.Algoritmo
                func = self.Sala_de_espera
                if self.serie:
                    self.serie = False
                    self.Cambiar()
            else:
                func = self.recordar[0]
                self.recordar = []
            if self.abierta:
                self.ventana.after(0, func)


    # This is where the AI sequence starts. The function checks to see how solved the Rubik's Cube is. If a certain step
    # is already complete, it will automatically scramble the cube. Then it selects which side will act as the top face
    # and proceeds to the next step, self.Primero().
    def Empezar(self):
        self.regla = 0
        self.regla_pequena = True
        declaracion = False
        for cero in range(6):
            subdeclaracion = True
            if self.cubo_de_roobit[cero][1] != cero:
                subdeclaracion = False
            elif self.cubo_de_roobit[cero][3] != cero:
                subdeclaracion = False
            elif self.cubo_de_roobit[cero][5] != cero:
                subdeclaracion = False
            elif self.cubo_de_roobit[cero][7] != cero:
                subdeclaracion = False
            for uno in range(4):
                norma = self.al_lado_des[cero][uno]
                if norma != self.cubo_de_roobit[self.al_lado_des[cero][uno]][self.de_al_lado_des[cero][uno][1]]:
                    subdeclaracion = False
            if subdeclaracion:
                declaracion = True
        if declaracion:
            self.regla = 0
            for cero in range(144):
                self.Girar_lado(random.randrange(6), random.choice([True, False]))
            self.Crear()
        self.base = random.randrange(6)
        self.util = self.al_lado_des[self.base]
        if self.tiempo == 0:
            numero = 0
        else:
            numero = 500
        if self.abierta:
            self.ventana.after(numero, self.Primero)


    # Determines whether rotating the top face would place an edge piece in the right location
    def Primero(self):
        if self.regla == 0:
            cero = 0
            while cero < 12:
                if self.base in self.p_a[2*cero]:
                    if self.p_a[2*cero].index(self.base) == 0:
                        if self.cubo_de_roobit[self.base][self.p_a[2*cero+1][0]] == self.base:
                            self.pertinente = (cero, 1)
                            cero = 13
                    else:
                        if self.cubo_de_roobit[self.base][self.p_a[2*cero+1][1]] == self.base:
                            self.pertinente = (cero, 0)
                            cero = 13
                cero+=1
            if cero == 14:
                self.vago = self.p_a[2*self.pertinente[0]][self.pertinente[1]]
                self.preciso = self.p_a[2*self.pertinente[0]+1][self.pertinente[1]]
                self.color = self.cubo_de_roobit[self.vago][self.preciso]
                func = self.Primeras_vueltas
            else:
                self.contando = 0
                self.color = self.util[0]
                func = self.Aristas_ultimas
            if self.abierta:
                self.ventana.after(0, func)


    # This function is only used if rotating the top face does in fact place an edge piece in the right location.
    def Primeras_vueltas(self):
        if self.regla == 0:
            if self.color != self.vago:
                self.vago = self.util[(self.util.index(self.vago) + 1) % 4]
                if (self.base, self.vago) in self.p_a:
                    self.preciso = self.p_a[self.p_a.index((self.base, self.vago)) + 1][1]
                else:
                    self.preciso = self.p_a[self.p_a.index((self.vago, self.base)) + 1][0]
                self.ra = (self.base, True)
                self.volver = self.Primeras_vueltas
                func = self.Sala_de_espera
                if self.serie:
                    self.serie = False
                    self.Cambiar()
            else:
                self.contando = 0
                self.color = self.util[0]
                func = self.Aristas_ultimas
            if self.abierta:
                self.ventana.after(0, func)


    # Places all the edge pieces that belong on the top face where they should be
    def Aristas_ultimas(self):
        if self.regla == 0:
            declaracion = True
            if self.recordar != []:
                for cero in range(len(self.recordar)):
                    if declaracion:
                        self.recordar[cero][0] -= 1
                        if self.recordar[cero][0] == 0:
                            declaracion = False
                            girar = (self.recordar[cero][1], self.recordar[cero][2])
                            self.recordar.pop(cero)
            if declaracion:
                cero = 0
                while cero < 24:
                    if self.cubo_de_roobit[self.p_a[cero][0]][self.p_a[cero + 1][0]] == self.base and \
                            self.cubo_de_roobit[self.p_a[cero][1]][self.p_a[cero + 1][1]] == self.color:
                        self.aqui = self.p_a[cero][0]
                        self.vago = self.p_a[cero][1]
                        cero = 24
                    elif self.cubo_de_roobit[self.p_a[cero][0]][self.p_a[cero + 1][0]] == self.color and \
                            self.cubo_de_roobit[self.p_a[cero][1]][self.p_a[cero + 1][1]] == self.base:
                        self.vago = self.p_a[cero][0]
                        self.aqui = self.p_a[cero][1]
                        cero = 24
                    else:
                        cero += 2
                if self.aqui == self.base:
                    if self.vago != self.color:
                        self.ra = (self.vago, True)
                        self.volver = self.Aristas_ultimas
                        func = self.Sala_de_espera
                        if self.serie:
                            self.serie = False
                            self.Cambiar()
                    else:
                        if self.contando < 3:
                            self.contando += 1
                            self.color = self.util[self.contando]
                            func = self.Aristas_ultimas
                        else:
                            self.contando = 0
                            self.color = self.util[0]
                            self.crayon = self.util[1]
                            func = self.Vertices_ultimas
                elif self.vago == self.base:
                    self.ra = (self.aqui, True)
                    self.volver = self.Aristas_ultimas
                    func = self.Sala_de_espera
                    if self.serie:
                        self.serie = False
                        self.Cambiar()
                elif self.aqui == (self.base+3)%6:
                    if self.vago != self.color:
                        self.ra = (self.aqui, True)
                    else:
                        self.ra = (self.vago, True)
                    self.volver = self.Aristas_ultimas
                    func = self.Sala_de_espera
                    if self.serie:
                        self.serie = False
                        self.Cambiar()
                elif self.vago == (self.base+3)%6:
                    if self.aqui == self.util[(self.util.index(self.color)-1)%4]:
                        self.ra = (self.aqui, True)
                        self.recordar.append([2, self.aqui, False])
                    else:
                        self.ra = (self.vago, True)
                    self.volver = self.Aristas_ultimas
                    func = self.Sala_de_espera
                    if self.serie:
                        self.serie = False
                        self.Cambiar()
                else:
                    if self.vago == self.color:
                        if self.aqui == self.util[(self.util.index(self.vago)+1)%4]:
                            self.ra = (self.vago, True)
                        else:
                            self.ra = (self.vago, False)
                    else:
                        if self.aqui == self.util[(self.util.index(self.vago)+1)%4]:
                            self.ra = (self.vago, False)
                            self.recordar.append([2, self.vago, True])
                        else:
                            self.ra = (self.vago, True)
                            self.recordar.append([2, self.vago, False])
                    self.volver = self.Aristas_ultimas
                    func = self.Sala_de_espera
                    if self.serie:
                        self.serie = False
                        self.Cambiar()
            else:
                self.ra = (girar[0], girar[1])
                self.volver = self.Aristas_ultimas
                func = self.Sala_de_espera
                if self.serie:
                    self.serie = False
                    self.Cambiar()
            if self.abierta:
                self.ventana.after(0, func)


    # Places all the corner pieces that belong on the top face where they should be
    def Vertices_ultimas(self):
        if self.regla == 0:
            cero = 0
            while cero < 16:
                grupo = (self.cubo_de_roobit[self.p_v[cero][0]][self.p_v[cero + 1][0]],
                         self.cubo_de_roobit[self.p_v[cero][1]][self.p_v[cero + 1][1]],
                         self.cubo_de_roobit[self.p_v[cero][2]][self.p_v[cero + 1][2]])
                if self.base in grupo and self.color in grupo and self.crayon in grupo:
                    caras = (self.p_v[cero][0], self.p_v[cero][1], self.p_v[cero][2])
                    self.aqui = caras[grupo.index(self.base)]
                    self.vago = caras[grupo.index(self.color)]
                    self.preciso = caras[grupo.index(self.crayon)]
                    cero = 16
                else:
                    cero+=2
            if self.aqui == self.base and self.vago == self.color and self.preciso == self.crayon:
                if self.contando < 3:
                    self.contando += 1
                    self.color = self.util[self.contando]
                    self.crayon = self.util[(self.contando+1)%4]
                    func = self.Vertices_ultimas
                else:
                    self.contando = 0
                    self.color = self.util[0]
                    self.crayon = self.util[1]
                    self.base = (self.base + 3) % 6
                    func = self.Medio
            elif self.aqui == self.base or self.vago == self.base or self.preciso == self.base:
                if self.aqui == self.base:
                    if self.vago == self.util[(self.util.index(self.preciso) + 1) % 4]:
                        self.pertinente = self.vago
                    else:
                        self.pertinente = self.preciso
                elif self.vago == self.base:
                    if self.aqui == self.util[(self.util.index(self.preciso) + 1) % 4]:
                        self.pertinente = self.aqui
                    else:
                        self.pertinente = self.preciso
                else:
                    if self.vago == self.util[(self.util.index(self.aqui) + 1) % 4]:
                        self.pertinente = self.vago
                    else:
                        self.pertinente = self.aqui
                self.recordar.append((self.pertinente, True))
                self.recordar.append(((self.base+3)%6, True))
                self.recordar.append(((self.base+3)%6, True))
                self.recordar.append((self.pertinente, False))
                self.recordar.append(self.Vertices_ultimas)
                func = self.Algoritmo
            elif self.aqui == (self.base+3)%6:
                if self.vago == self.crayon and self.preciso == self.color:
                    if self.vago == self.util[(self.util.index(self.preciso) + 1) % 4]:
                        self.pertinente = self.vago
                    else:
                        self.pertinente = self.preciso
                    self.recordar.append((self.pertinente, True))
                    self.recordar.append(((self.base+3)%6, True))
                    self.recordar.append(((self.base+3)%6, True))
                    self.recordar.append((self.pertinente, False))
                    self.recordar.append(self.Vertices_ultimas)
                    func = self.Algoritmo
                else:
                    self.ra = ((self.base + 3) % 6, True)
                    self.volver = self.Vertices_ultimas
                    func = self.Sala_de_espera
                    if self.serie:
                        self.serie = False
                        self.Cambiar()
            else:
                if self.vago == (self.base+3)%6:
                    self.pertinente = self.preciso
                    self.semaforo = self.crayon
                else:
                    self.pertinente = self.vago
                    self.semaforo = self.color
                if self.pertinente == self.semaforo:
                    if self.aqui == self.util[(self.util.index(self.pertinente) + 1) % 4]:
                        self.recordar.append(((self.base+3)%6, False))
                        self.recordar.append((self.pertinente, False))
                        self.recordar.append(((self.base+3)%6, True))
                        self.recordar.append((self.pertinente, True))
                        self.recordar.append(self.Vertices_ultimas)
                        func = self.Algoritmo
                    else:
                        self.recordar.append(((self.base+3)%6, True))
                        self.recordar.append((self.pertinente, True))
                        self.recordar.append(((self.base+3)%6, False))
                        self.recordar.append((self.pertinente, False))
                        self.recordar.append(self.Vertices_ultimas)
                        func = self.Algoritmo
                else:
                    self.ra = ((self.base + 3) % 6, True)
                    self.volver = self.Vertices_ultimas
                    func = self.Sala_de_espera
                    if self.serie:
                        self.serie = False
                        self.Cambiar()
            if self.abierta:
                self.ventana.after(0, func)


    # Places edge pieces that belong on the middle layer where they should go
    def Medio(self):
        if self.regla == 0:
            cero = 0
            while cero < 24:
                if self.cubo_de_roobit[self.p_a[cero][0]][self.p_a[cero + 1][0]] == self.crayon and \
                        self.cubo_de_roobit[self.p_a[cero][1]][self.p_a[cero + 1][1]] == self.color:
                    self.preciso = self.p_a[cero][0]
                    self.vago = self.p_a[cero][1]
                    cero = 24
                elif self.cubo_de_roobit[self.p_a[cero][0]][self.p_a[cero + 1][0]] == self.color and \
                        self.cubo_de_roobit[self.p_a[cero][1]][self.p_a[cero + 1][1]] == self.crayon:
                    self.vago = self.p_a[cero][0]
                    self.preciso = self.p_a[cero][1]
                    cero = 24
                else:
                    cero += 2
            if self.vago == self.base or self.preciso == self.base:
                if self.vago == self.base:
                    self.pertinente = self.preciso
                    self.semaforo = self.crayon
                    self.otro = self.color
                else:
                    self.pertinente = self.vago
                    self.semaforo = self.color
                    self.otro = self.crayon
                if self.pertinente == self.semaforo:
                    if self.otro == self.util[(self.util.index(self.semaforo) + 1) % 4]:
                        self.recordar.append((self.base, True))
                        self.recordar.append((self.otro, True))
                        self.recordar.append((self.base, False))
                        self.recordar.append((self.otro, False))
                        self.recordar.append((self.base, False))
                        self.recordar.append((self.semaforo, False))
                        self.recordar.append((self.base, True))
                        self.recordar.append((self.semaforo, True))
                        self.recordar.append(self.Medio)
                    else:
                        self.recordar.append((self.base, False))
                        self.recordar.append((self.otro, False))
                        self.recordar.append((self.base, True))
                        self.recordar.append((self.otro, True))
                        self.recordar.append((self.base, True))
                        self.recordar.append((self.semaforo, True))
                        self.recordar.append((self.base, False))
                        self.recordar.append((self.semaforo, False))
                        self.recordar.append(self.Medio)
                    func = self.Algoritmo
                else:
                    self.ra = (self.base, True)
                    self.volver = self.Medio
                    func = self.Sala_de_espera
                    if self.serie:
                        self.serie = False
                        self.Cambiar()
            else:
                if self.vago != self.color or self.preciso != self.crayon:
                    if self.vago == self.util[(self.util.index(self.preciso) + 1) % 4]:
                        self.semaforo = self.preciso
                        self.otro = self.vago
                    else:
                        self.semaforo = self.vago
                        self.otro = self.preciso
                    self.recordar.append((self.base, True))
                    self.recordar.append((self.otro, True))
                    self.recordar.append((self.base, False))
                    self.recordar.append((self.otro, False))
                    self.recordar.append((self.base, False))
                    self.recordar.append((self.semaforo, False))
                    self.recordar.append((self.base, True))
                    self.recordar.append((self.semaforo, True))
                    self.recordar.append(self.Medio)
                    func = self.Algoritmo
                else:
                    if self.contando < 3:
                        self.contando += 1
                        self.color = self.util[self.contando]
                        self.crayon = self.util[(self.contando + 1) % 4]
                        func = self.Medio
                    else:
                        func = self.Cruz
            if self.abierta:
                self.ventana.after(0, func)


    # Makes a cross with the edges on the bottom face
    def Cruz(self):
        if self.regla == 0:
            p_1 = self.cubo_de_roobit[self.base][1]
            p_3 = self.cubo_de_roobit[self.base][3]
            p_5 = self.cubo_de_roobit[self.base][5]
            p_7 = self.cubo_de_roobit[self.base][7]
            if p_1 == p_3 == p_5 == p_7:
                func = self.Esquinas
            elif p_1 == p_7 or p_3 == p_5:
                if p_1 == p_7:
                    self.pertinente = self.a_d[(self.base, 3)]
                else:
                    self.pertinente = self.a_d[(self.base, 1)]
                self.otro = self.util[(self.util.index(self.pertinente) + 1) % 4]
                self.recordar.append((self.pertinente, True))
                self.recordar.append((self.otro, True))
                self.recordar.append((self.base, True))
                self.recordar.append((self.otro, False))
                self.recordar.append((self.base, False))
                self.recordar.append((self.pertinente, False))
                self.recordar.append(self.Cruz)
                func = self.Algoritmo
            else:
                if p_1 == p_3:
                    if self.a_d[(self.base, 1)] == self.util[(self.util.index(self.a_d[(self.base, 3)]) + 1) % 4]:
                        self.pertinente = self.a_d[(self.base, 5)]
                    else:
                        self.pertinente = self.a_d[(self.base, 7)]
                elif p_5 == p_7:
                    if self.a_d[(self.base, 5)] == self.util[(self.util.index(self.a_d[(self.base, 7)]) + 1) % 4]:
                        self.pertinente = self.a_d[(self.base, 1)]
                    else:
                        self.pertinente = self.a_d[(self.base, 3)]
                elif p_3 == p_7:
                    if self.a_d[(self.base, 3)] == self.util[(self.util.index(self.a_d[(self.base, 7)]) + 1) % 4]:
                        self.pertinente = self.a_d[(self.base, 1)]
                    else:
                        self.pertinente = self.a_d[(self.base, 5)]
                elif p_1 == p_5:
                    if self.a_d[(self.base, 1)] == self.util[(self.util.index(self.a_d[(self.base, 5)]) + 1) % 4]:
                        self.pertinente = self.a_d[(self.base, 3)]
                    else:
                        self.pertinente = self.a_d[(self.base, 7)]
                else:
                    self.pertinente = (self.base + 1) % 6
                self.otro = self.util[(self.util.index(self.pertinente) + 1) % 4]
                self.recordar.append((self.pertinente, True))
                self.recordar.append((self.base, True))
                self.recordar.append((self.otro, True))
                self.recordar.append((self.base, False))
                self.recordar.append((self.otro, False))
                self.recordar.append((self.pertinente, False))
                self.recordar.append(self.Cruz)
                func = self.Algoritmo
            if self.abierta:
                self.ventana.after(0, func)


    # Solves the bottom face so that it is one color
    def Esquinas(self):
        if self.regla == 0:
            p_0 = self.cubo_de_roobit[self.base][0]
            p_2 = self.cubo_de_roobit[self.base][2]
            p_6 = self.cubo_de_roobit[self.base][6]
            p_8 = self.cubo_de_roobit[self.base][8]
            if p_0 == p_2 == p_6 == p_8:
                func = self.Penultima
            else:
                self.contando = 0
                if p_0 == self.base:
                    self.contando+=1
                if p_2 == self.base:
                    self.contando+=1
                if p_6 == self.base:
                    self.contando+=1
                if p_8 == self.base:
                    self.contando+=1
                if self.contando == 2:
                    cero = 0
                    while cero < 4:
                        cara_1 = self.al_lado_des[self.base][cero]
                        cara_2 = self.al_lado_des[self.base][(cero+1)%4]
                        uno = 0
                        while uno < 16:
                            if cara_1 in self.p_v[uno] and cara_2 in self.p_v[uno] and self.base in self.p_v[uno]:
                                termino = self.p_v[uno+1][self.p_v[uno].index(cara_1)]
                                uno = 16
                            else:
                                uno += 2
                        if self.cubo_de_roobit[cara_1][termino] == self.base:
                            cero = 4
                            self.pertinente = (cara_2 + 3) % 6
                        else:
                            cero += 1
                elif self.contando == 0:
                    cero = 0
                    while cero < 4:
                        cara_1 = self.al_lado_des[self.base][cero]
                        cara_2 = self.al_lado_des[self.base][(cero-1)%4]
                        uno = 0
                        while uno < 16:
                            if cara_1 in self.p_v[uno] and cara_2 in self.p_v[uno] and self.base in self.p_v[uno]:
                                termino = self.p_v[uno+1][self.p_v[uno].index(cara_1)]
                                uno = 16
                            else:
                                uno += 2
                        if self.cubo_de_roobit[cara_1][termino] == self.base:
                            cero = 4
                            self.pertinente = (cara_1 + 3) % 6
                        else:
                            cero += 1
                elif p_0 == self.base:
                    self.pertinente = (self.v_d[(self.base, 0)][0] + 3) % 6
                elif p_2 == self.base:
                    self.pertinente = (self.v_d[(self.base, 2)][0] + 3) % 6
                elif p_6 == self.base:
                    self.pertinente = (self.v_d[(self.base, 6)][0] + 3) % 6
                else:
                    self.pertinente = (self.v_d[(self.base, 8)][0] + 3) % 6
                self.recordar.append((self.pertinente, True))
                self.recordar.append((self.base, True))
                self.recordar.append((self.pertinente, False))
                self.recordar.append((self.base, True))
                self.recordar.append((self.pertinente, True))
                self.recordar.append((self.base, True))
                self.recordar.append((self.base, True))
                self.recordar.append((self.pertinente, False))
                self.recordar.append(self.Esquinas)
                func = self.Algoritmo
            if self.abierta:
                self.ventana.after(0, func)


    # Places the corner pieces that are on the bottom layer where they belong
    def Penultima(self):
        if self.regla == 0:
            lista = []
            self.contando = 0
            for cero in range(4):
                cara = self.al_lado_des[self.base][cero]
                if self.cubo_de_roobit[cara][self.de_al_lado_des[self.base][cero][0]] == cara:
                    self.contando += 1
                    lista.append(cara)
                if self.cubo_de_roobit[cara][self.de_al_lado_des[self.base][cero][2]] == cara:
                    self.contando += 1
                    lista.append(cara)
            if self.contando == 8:
                func = self.Ultima
            elif self.contando > 3:
                if lista.count(lista[0]) == 2:
                    self.pertinente = lista[0]
                elif lista.count(lista[1]) == 2:
                    self.pertinente = lista[1]
                elif lista.count(lista[2]) == 2:
                    self.pertinente = lista[2]
                else:
                    self.pertinente = lista[3]
                self.otro = self.util[(self.util.index(self.pertinente) - 1) % 4]
                self.recordar.append((self.otro, False))
                self.recordar.append(((self.pertinente + 3) % 6, True))
                self.recordar.append((self.otro, False))
                self.recordar.append((self.pertinente, True))
                self.recordar.append((self.pertinente, True))
                self.recordar.append((self.otro, True))
                self.recordar.append(((self.pertinente + 3) % 6, False))
                self.recordar.append((self.otro, False))
                self.recordar.append((self.pertinente, True))
                self.recordar.append((self.pertinente, True))
                self.recordar.append((self.otro, True))
                self.recordar.append((self.otro, True))
                self.recordar.append((self.base, False))
                self.recordar.append(self.Penultima)
                func = self.Algoritmo
            else:
                self.ra = (self.base, True)
                self.volver = self.Penultima
                func = self.Sala_de_espera
                if self.serie:
                    self.serie = False
                    self.Cambiar()
            if self.abierta:
                self.ventana.after(0, func)


    # Places the edge pieces that are on the bottom layer where they belong. This complete's the Rubiks Cube.
    def Ultima(self):
        if self.regla == 0:
            lista = []
            contando = 0
            for cero in range(4):
                cara = self.al_lado_des[self.base][cero]
                if self.cubo_de_roobit[cara][self.de_al_lado_des[self.base][cero][1]] == cara:
                    contando += 1
                    lista.append(cara)
            if contando == 4:
                self.tiempo = 180
                self.resolver.configure(text="Solve")
                self.rapido.configure(bg="#A0FFFF", relief="raised")
                self.regla = 1
            else:
                if contando == 0:
                    pertinente = self.util[0]
                    otro = self.util[1]
                    declaracion = True
                else:
                    pertinente = (lista[0] + 3) % 6
                    otro = self.util[(self.util.index(pertinente) + 1) % 4]
                    lugar = self.al_lado_des[self.base].index(otro)
                    declaracion = (pertinente == self.cubo_de_roobit[otro][self.de_al_lado_des[self.base][lugar][1]])
                self.recordar.append((pertinente, True))
                self.recordar.append((pertinente, True))
                self.recordar.append((self.base, declaracion))
                self.recordar.append(((otro+3)%6, True))
                self.recordar.append((otro, False))
                self.recordar.append((pertinente, True))
                self.recordar.append((pertinente, True))
                self.recordar.append(((otro+3)%6, False))
                self.recordar.append((otro, True))
                self.recordar.append((self.base, declaracion))
                self.recordar.append((pertinente, True))
                self.recordar.append((pertinente, True))
                self.recordar.append(self.Ultima)
                if self.abierta:
                    self.ventana.after(0, self.Algoritmo)



    #           BUTTONS AND CONTROLS

    # Decides what function to call based on where the screen is clicked. It is responsible for determining whether the
    # user is dragging the cube as well as any button clicks (when the Instruction menu is closed).
    def Raton(self, event):
        if self.abierta:
            equis = self.ventana.winfo_pointerx() - self.ventana.winfo_rootx()
            igriega = self.ventana.winfo_pointery() - self.ventana.winfo_rooty()
            if -1 < equis < 512 and -1 < igriega < 512:
                if self.activar:
                    self.activar = False
                    self.ventana.unbind("<Motion>")
                else:
                    self.activar = True
                    self.x = self.ventana.winfo_pointerx()
                    self.y = self.ventana.winfo_pointery()
                    self.ventana.bind("<Motion>", self.Interpretar)
            elif 559 < igriega < 595:
                declaracion = False
                if 51 < equis < 168:
                    declaracion = True
                    self.instrucciones.configure(bg="#70C8C8", relief="flat")
                    func = self.Pequena_i
                elif 217 < equis < 288:
                    declaracion = True
                    self.resolver.configure(bg="#70C8C8", relief="flat")
                    func = self.Intro
                elif 338 < equis < 459 and self.regla == 1:
                    declaracion = True
                    self.rapido.configure(bg="#70C8C8", relief="flat")
                    func = self.Rapido
                if declaracion and self.abierta:
                    self.ventana.after(144, func)


    # This is the "drag" function. It rotates the cube based on the direction in which the mouse moves.
    def Interpretar(self, event):
        if self.abierta:
            if self.rg == None and ((abs(self.x - self.ventana.winfo_pointerx()) >= 2 or
                                     abs(self.y - self.ventana.winfo_pointery()) >= 2)):
                self.regla_pequena = False
                largo_x = self.ventana.winfo_pointerx() - self.x
                largo_y = self.ventana.winfo_pointery() - self.y
                self.x = self.ventana.winfo_pointerx()
                self.y = self.ventana.winfo_pointery()
                if largo_x != 0:
                    if largo_x < 0:
                        conv_x = 1
                    else:
                        conv_x = -1
                    if largo_y < 0:
                        conv_y = -1
                    else:
                        conv_y = 1
                    lejos = (largo_y ** 2 + largo_x ** 2) ** 0.5
                    self.rg = (0.05, conv_y * abs(largo_y/lejos), conv_x * abs(largo_x/lejos))
                elif largo_y < 0:
                    self.rg = (0.05, -1, 0)
                else:
                    self.rg = (0.05, 1, 0)
                self.regla_pequena = True
                if self.serie and self.abierta:
                    self.serie = False
                    self.ventana.after(0, self.Cambiar)


    # Opens and closes the Instruction menu. Also activates and deactivates buttons and key presses accordingly.
    def Instrucciones(self):
        if self.regla_pequena and self.abierta:
            self.regla = 1
            self.tiempo = 180
            self.recordar = []
            self.resolver.configure(text="Solve")
            self.rapido.configure(bg="#A0FFFF", relief="raised")
            self.activar = False
            self.ventana.unbind("<Motion>")
            self.ventana.unbind("<Button-1>")
            self.ventana.unbind("<space>")
            self.ventana.unbind("<Return>")
            self.ventana.unbind("2")
            self.ventana.unbind("3")
            self.ventana.unbind("c")
            self.ventana.unbind("x")
            self.ventana.unbind("r")
            self.ventana.unbind("f")
            self.ventana.unbind("q")
            self.ventana.unbind("a")
            self.ventana.unbind("e")
            self.ventana.unbind("w")
            self.ventana.unbind("d")
            self.ventana.unbind("s")
            self.ventana.unbind("@")
            self.ventana.unbind("#")
            self.ventana.unbind("C")
            self.ventana.unbind("X")
            self.ventana.unbind("R")
            self.ventana.unbind("F")
            self.ventana.unbind("Q")
            self.ventana.unbind("A")
            self.ventana.unbind("E")
            self.ventana.unbind("W")
            self.ventana.unbind("D")
            self.ventana.unbind("S")
            self.espacio.delete("all")
            self.ventana.bind("<Button-1>", self.Avanzar)
            self.espacio.pack_forget()
            self.s_som.place_forget()
            self.p_som.place_forget()
            self.resolver.place_forget()
            self.rapido.place_forget()
            self.texto.configure(text=self.pagina_1)
            self.boton_de_pagina.configure(text="Next", font=("Helvetica", 15))
            self.mas_alla.place(height=482, width=482, y=15, x=15)
            self.perfil.place(height=480, width=480, y=16, x=16)
            self.texto.place(height=464, width=464, y=24, x=24)
            self.menos_alla.place(height=466, width=466, y=23, x=23)
            self.perfil.lift()
            self.menos_alla.lift()
            self.texto.lift()
            self.boton_de_pagina.place(height=31, width=55, y=436, x=408)
            self.boton_de_pagina.lift()
            self.i_som.place(height=37, width=78, y=45, x=215)
            self.instrucciones.place(height=35, width=76, y=46, x=216)
            self.instrucciones.configure(text="Return")
            self.ventana.update()
            self.regla_pequena = False
        elif self.abierta:
            self.mas_alla.place_forget()
            self.perfil.place_forget()
            self.texto.place_forget()
            self.menos_alla.place_forget()
            self.boton_de_pagina.place_forget()
            if self.boton_de_pagina["text"] == "Back":
                self.teclado_0.place_forget()
                self.teclado_1.place_forget()
                self.teclado_2.place_forget()
                self.teclado_3.place_forget()
            self.espacio.pack()
            self.ventana.unbind("<Button-1>")
            self.Boton()
            self.i_som.place(height=37, width=116, y=45, x=50)
            self.s_som.place(height=37, width=70, y=45, x=216)
            self.p_som.place(height=37, width=122, y=45, x=336)
            self.instrucciones.place(height=35, width=114, y=46, x=51)
            self.instrucciones.lift()
            self.resolver.place(height=35, width=68, y=46, x=217)
            self.resolver.lift()
            self.rapido.place(height=35, width=120, y=46, x=337)
            self.rapido.lift()
            self.instrucciones.configure(text="Instructions")
            self.Crear()
            self.ventana.update()
            self.regla_pequena = True


    # Determines what button is clicked when the Instruction menu is up
    def Avanzar(self, event):
        if self.abierta:
            equis = self.ventana.winfo_pointerx() - self.ventana.winfo_rootx()
            igriega = self.ventana.winfo_pointery() - self.ventana.winfo_rooty()
            declaracion = False
            if 435 < igriega < 467 and 407 < equis < 463:
                declaracion = True
                self.boton_de_pagina.configure(bg="#00D0D0")
                func = self.Pequena_bdp
            elif 559 < igriega < 595 and 217 < equis < 294:
                declaracion = True
                self.instrucciones.configure(bg="#70C8C8", relief="flat")
                func = self.Pequena_i
            if declaracion and self.abierta:
                self.ventana.after(144, func)


    # Changes the page when the "Next" or "Back" button is clicked
    def Pequena_bdp(self):
        self.boton_de_pagina.configure(bg="#00FFFF")
        if self.boton_de_pagina["text"] == "Next" and self.abierta:
            self.texto.configure(text=self.pagina_2)
            self.boton_de_pagina.configure(text="Back")
            self.teclado_0.lift()
            self.teclado_1.lift()
            self.teclado_2.lift()
            self.teclado_3.lift()
            self.teclado_0.place(x=228, y=87)
            self.teclado_1.place(x=196, y=117)
            self.teclado_2.place(x=196, y=147)
            self.teclado_3.place(x=228, y=177)
            self.ventana.update()
        elif self.abierta:
            self.texto.configure(text=self.pagina_1)
            self.boton_de_pagina.configure(text="Next")
            self.teclado_0.place_forget()
            self.teclado_1.place_forget()
            self.teclado_2.place_forget()
            self.teclado_3.place_forget()


    # Closes the instruction menu after "Return" is clicked
    def Pequena_i(self):
        self.instrucciones.configure(bg="#A0FFFF", relief="raised")
        if self.abierta:
            self.ventana.after(0, self.Instrucciones)


    # Activates when "Solve" is clicked. Starts the AI solving process (with animation).
    def Intro(self):
        self.resolver.configure(bg="#A0FFFF", relief="raised")
        if self.regla == 0 and self.resolver["text"] == "Stop":
            self.regla = 1
            if self.tiempo == 0:
                self.muy_pequena = False
                self.tiempo = 180
            self.recordar = []
            self.resolver.configure(text="Solve")
            self.rapido.configure(bg="#A0FFFF", relief="raised")
        elif self.regla == 1:
            self.resolver.configure(text="Stop")
            self.rapido.configure(bg="#70C8C8", relief="flat")
            if self.abierta:
                self.ventana.after(0, self.Empezar)


    # Activates when "Quick Solve" is clicked. Starts the AI solving process (without animation).
    def Rapido(self):
        self.resolver.configure(text="Stop")
        self.tiempo = 0
        if self.abierta:
            self.ventana.after(0, self.Empezar)


    # Scrambles the cube when the space key is pressed
    def Cifrar(self, event):
        if self.regla == 1:
            self.regla = 0
            for cero in range(144):
                self.Girar_lado(random.randrange(6), random.choice([True, False]))
            if self.serie:
                self.Crear()
            self.regla = 1


    # Changes the lighting effects when the Enter key is pressed
    def Brillo(self, event):
        if self.contraste:
            self.contraste = False
            self.conversion = ["#FFFFFF", "#0080FF", "#FF0000", "#FFFF00", "#00FF80", "#FF9000"]
        else:
            self.contraste = True
            self.conversion = ["#C0C0C0", "#0060C0", "#C00000", "#C0C000", "#00C060", "#C06C00"]
        if self.serie and self.abierta:
            self.ventana.after(0, self.Crear)


    # The following twelve commands are named after their respective keys. The instructions explain what they do.

    def E(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            numero = self.verdad[2]
            self.ra = (numero, True)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def W(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            numero = self.verdad[2]
            self.ra = (numero, False)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def D(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            numero = (self.verdad[2] + 3) % 6
            self.ra = (numero, False)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def S(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            numero = (self.verdad[2] + 3) % 6
            self.ra = (numero, True)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def X(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            self.Ay_caramba()
            numero = self.ay
            self.ra = (numero, True)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def N2(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            self.Ay_caramba()
            numero = self.ay
            self.ra = (numero, False)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def N3(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            self.Ay_caramba()
            numero = (self.ay + 3) % 6
            self.ra = (numero, True)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def C(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            self.Ay_caramba()
            numero = (self.ay + 3) % 6
            self.ra = (numero, False)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def Q(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            self.Ay_caramba()
            numero = self.caramba
            self.ra = (numero, True)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def R(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            self.Ay_caramba()
            numero = self.caramba
            self.ra = (numero, False)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def F(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            self.Ay_caramba()
            numero = (self.caramba + 3) % 6
            self.ra = (numero, True)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)

    def A(self, event):
        if self.regla == 1 and self.ra == None:
            self.regla = 2
            self.Ay_caramba()
            numero = (self.caramba + 3) % 6
            self.ra = (numero, False)
            if self.serie and self.abierta:
                self.ventana.after(0, self.Cambiar)



    #           SETUP

    # Assigns commands to onscreen buttons and creates text boxes. It is only called once at the beginning.
    def Primero_Boton(self):
        color = "#A0FFFF"
        crayon = "#FFFFFF"
        self.instrucciones = tk.Label(self.marco, font = ("Helvetica", 18), bg=color, relief="raised", bd=3,
                                      text="Instructions")
        self.resolver = tk.Label(self.marco, font=("Helvetica", 18), bg=color, text="Solve", relief="raised", bd=3)
        self.rapido = tk.Label(self.marco, font=("Helvetica", 18), text="Quick Solve", bg=color, relief="raised", bd=3)
        self.i_som = tk.Label(self.marco, bg="#000000")
        self.i_som.place(height=37, width=116, y=45, x=50)
        self.s_som = tk.Label(self.marco, bg="#000000")
        self.s_som.place(height=37, width=70, y=45, x=216)
        self.p_som = tk.Label(self.marco, bg="#000000")
        self.p_som.place(height=37, width=122, y=45, x=336)
        self.instrucciones.place(height=35, width=114, y=46, x=51)
        self.instrucciones.lift()
        self.resolver.place(height=35, width=68, y=46, x=217)
        self.resolver.lift()
        self.rapido.place(height=35, width=120, y=46, x=337)
        self.rapido.lift()
        self.mas_alla = tk.Label(self.estuche, bg="#000000")
        self.menos_alla = tk.Label(self.estuche, bg="#000000")
        self.boton_de_pagina = tk.Label(self.estuche, bg="#00FFFF", bd=2, relief="raised", text="Next")
        self.perfil = tk.Label(self.estuche, bg="#FFA000")
        self.texto = tk.Label(self.estuche, font=("Helvetica", 18), bg=crayon, fg="#000000", justify=tk .LEFT)
        self.teclado_0 = tk.Label(self.estuche, font=("Courier", 18), bg=crayon, text="2  3")
        self.teclado_1 = tk.Label(self.estuche, font=("Courier", 18), bg=crayon, text="Q  W  E  R")
        self.teclado_2 = tk.Label(self.estuche, font=("Courier", 18), bg=crayon, text="A  S  D  F")
        self.teclado_3 = tk.Label(self.estuche, font=("Courier", 18), bg=crayon, text="X  C")


    # Assigns commands to key presses and the screen click. It is called once at the beginning and whenever the
    # instruction menu is closed.
    def Boton(self):
        self.ventana.bind("<Button-1>", self.Raton)
        self.ventana.bind("<space>", self.Cifrar)
        self.ventana.bind("<Return>", self.Brillo)
        self.ventana.bind("2", self.N2)
        self.ventana.bind("3", self.N3)
        self.ventana.bind("c", self.C)
        self.ventana.bind("x", self.X)
        self.ventana.bind("r", self.R)
        self.ventana.bind("f", self.F)
        self.ventana.bind("q", self.Q)
        self.ventana.bind("a", self.A)
        self.ventana.bind("e", self.E)
        self.ventana.bind("w", self.W)
        self.ventana.bind("d", self.D)
        self.ventana.bind("s", self.S)
        self.ventana.bind("@", self.N2)
        self.ventana.bind("#", self.N3)
        self.ventana.bind("C", self.C)
        self.ventana.bind("X", self.X)
        self.ventana.bind("R", self.R)
        self.ventana.bind("F", self.F)
        self.ventana.bind("Q", self.Q)
        self.ventana.bind("A", self.A)
        self.ventana.bind("E", self.E)
        self.ventana.bind("W", self.W)
        self.ventana.bind("D", self.D)
        self.ventana.bind("S", self.S)


    # Creates and stores data required for the program, most of which is numerical. It is only called once at the
    # beginning. Note that locations of points on the cube are recorded as quaternions, with i, j, k values acting as
    # x, y, z coordinates. Sometimes a real value of 0 will precede these coordinates; this only occurs when doing so
    # aids in quaternion multiplication. The instructions are also written here.
    def Sistema(self):
        self.abierta = True
        self.serie = True
        self.rg = None
        self.ra = None
        self.volver = None
        self.regla = 1
        self.regla_pequena = True
        self.muy_pequena = True
        self.contraste = True
        self.activar = False
        self.circunferencia = 0
        self.tiempo = 180
        self.recordar = []
        self.conversion = ["#C0C0C0", "#0060C0", "#C00000", "#C0C000", "#00C060", "#C06C00"]
        self.cubo_de_roobit = [[0]*9, [1]*9, [2]*9, [3]*9, [4]*9, [5]*9]
        self.transicion = [False]*6
        self.caras = [[0, 2, 6, 4], [0, 1, 3, 2], [0, 1, 5, 4], [1, 3, 7, 5], [4, 5, 7, 6], [2, 3, 7, 6]]
        self.bloque = [[0, 6, 18, 12], [2, 5, 11, 8], [1, 4, 16, 13], [3, 9, 21, 15], [14, 17, 23, 20], [7, 10, 22, 19]]
        self.al_lado_des = [[1, 2, 4, 5], [3, 2, 0, 5], [0, 1, 3, 4], [5, 4, 2, 1], [5, 0, 2, 3], [4, 3, 1, 0]]
        self.de_al_lado_des = [[[2, 1, 0], [0, 1, 2], [0, 1, 2], [2, 1, 0]],
                               [[6, 3, 0], [6, 3, 0], [0, 3, 6], [0, 3, 6]],
                               [[2, 1, 0], [0, 3, 6], [0, 1, 2], [6, 3, 0]],
                               [[6, 7, 8], [8, 7, 6], [8, 7, 6], [6, 7, 8]],
                               [[2, 5, 8], [2, 5, 8], [8, 5, 2], [8, 5, 2]],
                               [[2, 5, 8], [8, 7, 6], [8, 5, 2], [6, 7, 8]]]
        self.p_a = ((0, 1), (3, 1), (0, 2), (1, 1), (0, 4), (5, 1), (0, 5), (7, 1), (1, 2), (3, 3), (1, 5), (5, 3),
                    (4, 2), (3, 5), (4, 5), (5, 5), (3, 1), (3, 7), (3, 2), (1, 7), (3, 4), (5, 7), (3, 5), (7, 7))
        self.p_v = ((0, 1, 2), (0, 0, 0), (3, 1, 2), (0, 6, 6), (0, 4, 2), (2, 0, 2), (3, 4, 2), (2, 6, 8),
                    (0, 1, 5), (6, 2, 0), (3, 1, 5), (6, 8, 6), (0, 4, 5), (8, 2, 2), (3, 4, 5), (8, 8, 8))
        self.a_d = {(0, 3): 1, (1, 1): 0, (0, 1): 2, (2, 1): 0, (0, 5): 4, (4, 1): 0, (0, 7): 5, (5, 1): 0,
                    (1, 3): 2, (2, 3): 1, (1, 5): 5, (5, 3): 1, (4, 3): 2, (2, 5): 4, (4, 5): 5, (5, 5): 4,
                    (3, 3): 1, (1, 7): 3, (3, 1): 2, (2, 7): 3, (3, 5): 4, (4, 7): 3, (3, 7): 5, (5, 7): 3}
        self.v_d = {(0, 0): (2, 1), (1, 0): (0, 2), (2, 0): (1, 0), (3, 0): (1, 2), (1, 6): (2, 3), (2, 6): (3, 1),
                    (0, 2): (4, 2), (4, 0): (2, 0), (2, 2): (0, 4), (3, 2): (2, 4), (4, 6): (3, 2), (2, 8): (4, 3),
                    (0, 6): (1, 5), (1, 2): (5, 0), (5, 0): (0, 1), (3, 6): (5, 1), (1, 8): (3, 5), (5, 6): (1, 3),
                    (0, 8): (5, 4), (4, 2): (0, 5), (5, 2): (4, 0), (3, 8): (4, 5), (4, 8): (5, 3), (5, 8): (3, 4)}
        self.vectores = [[0, 0, 0, -1], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0]]
        self.centro = 0.3840410272734564
        b = 0.5773502691896257
        i = 0.5464207904830386
        m = 0.2165063509461097
        c = 0.1649572197684645
        g = 0.1907317853572871
        self.vertice = []
        self.filo = []
        for cero in range(-1, 2, 2):
            for uno in range(-1, 2, 2):
                for dos in range(-1, 2, 2):
                    self.vertice.append([0, cero * b, uno * b, dos * b])
                    self.filo.append([0, cero * b, uno * b, dos * g])
                    self.filo.append([0, cero * b, uno * g, dos * b])
                    self.filo.append([0, cero * g, uno * b, dos * b])
        self.ubicaciones = [[
                [[-i, -i, -b], [-m, -i, -b], [-m, -m, -b], [-i, -m, -b]],
                [[-c, -i, -b], [c, -i, -b], [c, -m, -b], [-c, -m, -b]],
                [[i, -i, -b], [m, -i, -b], [m, -m, -b], [i, -m, -b]],
                [[-i, -c, -b], [-m, -c, -b], [-m, c, -b], [-i, c, -b]],
                [[-c, -c, -b], [c, -c, -b], [c, c, -b], [-c, c, -b]],
                [[i, -c, -b], [m, -c, -b], [m, c, -b], [i, c, -b]],
                [[-i, i, -b], [-m, i, -b], [-m, m, -b], [-i, m, -b]],
                [[-c, i, -b], [c, i, -b], [c, m, -b], [-c, m, -b]],
                [[i, i, -b], [m, i, -b], [m, m, -b], [i, m, -b]]
            ], [
                [[-b, -i, -i], [-b, -m, -i], [-b, -m, -m], [-b, -i, -m]],
                [[-b, -c, -i], [-b, c, -i], [-b, c, -m], [-b, -c, -m]],
                [[-b, i, -i], [-b, m, -i], [-b, m, -m], [-b, i, -m]],
                [[-b, -i, -c], [-b, -m, -c], [-b, -m, c], [-b, -i, c]],
                [[-b, -c, -c], [-b, c, -c], [-b, c, c], [-b, -c, c]],
                [[-b, i, -c], [-b, m, -c], [-b, m, c], [-b, i, c]],
                [[-b, -i, i], [-b, -m, i], [-b, -m, m], [-b, -i, m]],
                [[-b, -c, i], [-b, c, i], [-b, c, m], [-b, -c, m]],
                [[-b, i, i], [-b, m, i], [-b, m, m], [-b, i, m]]
            ], [
                [[-i, -b, -i], [-m, -b, -i], [-m, -b, -m], [-i, -b, -m]],
                [[-c, -b, -i], [c, -b, -i], [c, -b, -m], [-c, -b, -m]],
                [[i, -b, -i], [m, -b, -i], [m, -b, -m], [i, -b, -m]],
                [[-i, -b, -c], [-m, -b, -c], [-m, -b, c], [-i, -b, c]],
                [[-c, -b, -c], [c, -b, -c], [c, -b, c], [-c, -b, c]],
                [[i, -b, -c], [m, -b, -c], [m, -b, c], [i, -b, c]],
                [[-i, -b, i], [-m, -b, i], [-m, -b, m], [-i, -b, m]],
                [[-c, -b, i], [c, -b, i], [c, -b, m], [-c, -b, m]],
                [[i, -b, i], [m, -b, i], [m, -b, m], [i, -b, m]]
            ], [
                [[-i, -i, b], [-m, -i, b], [-m, -m, b], [-i, -m, b]],
                [[-c, -i, b], [c, -i, b], [c, -m, b], [-c, -m, b]],
                [[i, -i, b], [m, -i, b], [m, -m, b], [i, -m, b]],
                [[-i, -c, b], [-m, -c, b], [-m, c, b], [-i, c, b]],
                [[-c, -c, b], [c, -c, b], [c, c, b], [-c, c, b]],
                [[i, -c, b], [m, -c, b], [m, c, b], [i, c, b]],
                [[-i, i, b], [-m, i, b], [-m, m, b], [-i, m, b]],
                [[-c, i, b], [c, i, b], [c, m, b], [-c, m, b]],
                [[i, i, b], [m, i, b], [m, m, b], [i, m, b]]
            ], [
                [[b, -i, -i], [b, -m, -i], [b, -m, -m], [b, -i, -m]],
                [[b, -c, -i], [b, c, -i], [b, c, -m], [b, -c, -m]],
                [[b, i, -i], [b, m, -i], [b, m, -m], [b, i, -m]],
                [[b, -i, -c], [b, -m, -c], [b, -m, c], [b, -i, c]],
                [[b, -c, -c], [b, c, -c], [b, c, c], [b, -c, c]],
                [[b, i, -c], [b, m, -c], [b, m, c], [b, i, c]],
                [[b, -i, i], [b, -m, i], [b, -m, m], [b, -i, m]],
                [[b, -c, i], [b, c, i], [b, c, m], [b, -c, m]],
                [[b, i, i], [b, m, i], [b, m, m], [b, i, m]]
            ], [
                [[-i, b, -i], [-m, b, -i], [-m, b, -m], [-i, b, -m]],
                [[-c, b, -i], [c, b, -i], [c, b, -m], [-c, b, -m]],
                [[i, b, -i], [m, b, -i], [m, b, -m], [i, b, -m]],
                [[-i, b, -c], [-m, b, -c], [-m, b, c], [-i, b, c]],
                [[-c, b, -c], [c, b, -c], [c, b, c], [-c, b, c]],
                [[i, b, -c], [m, b, -c], [m, b, c], [i, b, c]],
                [[-i, b, i], [-m, b, i], [-m, b, m], [-i, b, m]],
                [[-c, b, i], [c, b, i], [c, b, m], [-c, b, m]],
                [[i, b, i], [m, b, i], [m, b, m], [i, b, m]]
            ]]
        self.pagina_1 = \
"""Click the screen to start dragging the cube. Click again
to stop. (Drag at a fairly slow pace for better results.)

Click "Solve" to tell the computer to solve the cube
while showing every move it makes.

Click "Quick Solve" to tell the computer to solve the
cube in seconds. The methods used by "Solve" and
"Quick Solve" are the same, but "Quick Solve" does
not create complex animations.

Press the Space key to scramble the cube.

Press the Enter key to change the lighting effects. One
version creates a shadow, while the other only displays
bright colors.

See the next page for rotating each face of the cube
manually.\n\n"""
        self.pagina_2 = \
"""It may help to think of the following keys as forming a   
grid on your keyboard:\n\n\n\n\n\n
2:  turns the left side up
3:  turns the right side up
Q:  turns the top side left
W:  turns the front face counter-clockwise
E:  turns the front face clockwise
R:  turns the top side right
A:  turns the bottom side left
S:  turns the back face counter-clockwise
D:  turns the back face clockwise
F:  turns the bottom side right
X:  turns the left side down
C:  turns the right side down\n"""



# Calls the function at the very top of the script, which sets everything into motion.
principal()
