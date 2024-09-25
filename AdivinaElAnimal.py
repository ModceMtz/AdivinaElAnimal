import tkinter as tk
import random
from tkinter import messagebox


ANIMALES = [
    ('Leon', 'Depredador de la sabana.'),
    ('Caballo', 'Animal Equino.'),
    ('Tiburon', 'Depredador marino.'),
    ('Cebra', 'Animal rayado.'),
    ('Ajolote', 'Animal acuático endemico de Mexico.'),
    ('Camello', 'Animal jorobado.'),
    ('Gato', 'Mascota independiente.'),
    ('Serpiente', 'Reptil sin patas.'),
    ('Cocodrilo', 'Reptil que vive en ríos.'),
    ('Perro', 'El mejor amigo del hombre.'),
    ('Pinguino', 'Animal con traje.'),
    ('Ballena', 'Mamífero marino que canta.'),
    ('Elefante', 'Mamífero que jamás olvida.'),
    ('Lobo', 'Canino que caza en manada.'),
    ('Tortuga', 'Reptil acorazado.'),
    ('Tigre', 'Felino de gran tamaño.'),
    ('Capibara', 'Amigo de todos.'),
    ('Canguro', 'Animal boxeador.'),
    ('Aguila', 'Ave rapaz con vista aguda y gran cazadora.'),
    ('Murcielago', 'Mamífero volador.'),
    ('Morsa','Con colmillos prominentes y vive en aguas frías.'),
    ('Flamenco', 'Rosa por su dieta de crustáceos.'),
    ('Halcón','Velocidad y habilidad de caza en vuelo.'),
    ('Rinoceronte','Gran tamaño y piel gruesa.')
]



class AdivinaElAnimal:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Adivinanza de Animales")
        self.root.geometry("800x600")
        self.usuario = ""
        self.nivel_actual = 0
        self.puntaje_total = 0
        self.palabras_usadas = []
        self.vidas = 6
        self.palabra_actual = ""
        self.pista_actual = ""
        self.palabra_oculta = []
        self.intentos_fallidos = 0
        self.puntajes_usuarios = {}


        self.crear_interfaz_inicio()

    def crear_interfaz_inicio(self):

        for widget in self.root.winfo_children():
            widget.destroy()


        self.frame_inicio = tk.Frame(self.root)
        self.frame_inicio.pack()

        tk.Label(self.frame_inicio, text="Ingrese su nombre:").pack(pady=10)
        self.entry_usuario = tk.Entry(self.frame_inicio)
        self.entry_usuario.pack(pady=10)

        btn_nuevo_juego = tk.Button(self.frame_inicio, text="Comenzar Nuevo Juego", command=self.nuevo_juego)
        btn_nuevo_juego.pack(pady=10)

        btn_instrucciones = tk.Button(self.frame_inicio, text="Instrucciones", command=self.mostrar_instrucciones)
        btn_instrucciones.pack(pady=10)


        btn_puntuacion = tk.Button(self.frame_inicio, text="Ver Puntuación", command=self.mostrar_puntuacion)
        btn_puntuacion.pack(pady=10)

    def mostrar_instrucciones(self):

        messagebox.showinfo("Instrucciones", "Adivina el animal letra por letra. Tienes 6 vidas por palabra.")

    def mostrar_puntuacion(self):

        puntuacion_texto = "Puntuación de usuarios:\n"
        if self.puntajes_usuarios:
            for usuario, puntajes in self.puntajes_usuarios.items():
                puntuacion_texto += f"\nUsuario: {usuario}\n"
                puntuacion_texto += "Puntuación por nivel:\n"
                for i, puntaje in enumerate(puntajes["niveles"], 1):
                    puntuacion_texto += f"Nivel {i}: {puntaje} puntos\n"
                puntuacion_texto += f"Puntuación total: {puntajes['total']} puntos\n"
        else:
            puntuacion_texto += "No hay puntuaciones registradas aún."

        messagebox.showinfo("Puntuación", puntuacion_texto)

    def nuevo_juego(self):
        self.usuario = self.entry_usuario.get()
        if self.usuario:
            self.mostrar_instrucciones()
            self.nivel_actual = 1
            self.puntaje_total = 0
            self.palabras_usadas = []
            self.vidas = 6
            self.intentos_fallidos = 0
            self.frame_inicio.pack_forget()
            self.jugar_nivel()


            if self.usuario not in self.puntajes_usuarios:
                self.puntajes_usuarios[self.usuario] = {"niveles": [], "total": 0}
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un nombre de usuario.")

    def jugar_nivel(self):

        if self.nivel_actual <= 10:
            self.palabra_actual, self.pista_actual = random.choice(
                [p for p in ANIMALES if p[0] not in self.palabras_usadas])
            self.palabras_usadas.append(self.palabra_actual)
            self.palabra_oculta = ["_" for _ in self.palabra_actual]
            self.vidas = 6
            self.crear_interfaz_juego()
        else:
            messagebox.showinfo("Juego Terminado", f"¡Felicidades {self.usuario}! Has completado el juego.")
            self.regresar_inicio()

    def crear_interfaz_juego(self):

        self.frame_juego = tk.Frame(self.root)
        self.frame_juego.pack()

        tk.Label(self.frame_juego, text=f"Nivel {self.nivel_actual}").pack(pady=10)
        tk.Label(self.frame_juego, text=f"Pista: {self.pista_actual}").pack(pady=10)
        self.lbl_palabra_oculta = tk.Label(self.frame_juego, text=' '.join(self.palabra_oculta))
        self.lbl_palabra_oculta.pack(pady=10)


        self.lbl_vidas = tk.Label(self.frame_juego, text=f"Vidas restantes: {self.vidas}")
        self.lbl_vidas.pack(pady=10)

        self.entry_letra = tk.Entry(self.frame_juego)
        self.entry_letra.pack(pady=10)

        btn_adivinar = tk.Button(self.frame_juego, text="Adivinar Letra", command=self.adivinar_letra)
        btn_adivinar.pack(pady=10)

    def adivinar_letra(self):
        letra = self.entry_letra.get().upper()


        if len(letra) != 1 or not letra.isalpha():
            messagebox.showwarning("Advertencia", "Por favor, ingresa solo una letra.")
            self.entry_letra.delete(0, tk.END)
            return


        self.entry_letra.delete(0, tk.END)

        if letra in self.palabra_actual.upper():
            self.actualizar_palabra_oculta(letra)
        else:
            self.intentos_fallidos += 1
            self.vidas -= 1


        self.lbl_vidas.config(text=f"Vidas restantes: {self.vidas}")

        if "_" not in self.palabra_oculta:
            messagebox.showinfo("Correcto", "¡Has adivinado la palabra!")
            puntaje_nivel = (6 - self.intentos_fallidos) * 10
            self.puntajes_usuarios[self.usuario]["niveles"].append(puntaje_nivel)
            self.puntajes_usuarios[self.usuario]["total"] += puntaje_nivel
            self.nivel_actual += 1
            self.frame_juego.pack_forget()
            self.jugar_nivel()
        elif self.vidas == 0:
            messagebox.showinfo("Perdiste", "¡Te has quedado sin vidas!")
            self.puntajes_usuarios[self.usuario]["niveles"].append(0)
            self.frame_juego.pack_forget()
            self.regresar_inicio()

    def actualizar_palabra_oculta(self, letra):
        for idx, char in enumerate(self.palabra_actual.upper()):
            if char == letra:
                self.palabra_oculta[idx] = letra
        self.lbl_palabra_oculta.config(text=' '.join(self.palabra_oculta))

    def regresar_inicio(self):

        messagebox.showinfo("Juego Terminado", f"Juego terminado, regresando al menú de inicio")
        self.crear_interfaz_inicio()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdivinaElAnimal(root)
    root.mainloop()
