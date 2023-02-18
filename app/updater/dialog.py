import tkinter as tk


def dialog_error(error):
    """
    Error displayed, based on :
    https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/18d8fbe8-a967-4f1c-ae50-99ca8e491d2d

    Args:
        - ():
    """
    error_type = type(error).__name__
    error_message = error.args[0]
    # Créer une instance de fenêtre
    window = tk.Tk()

    # Définir le titre de la fenêtre
    window.title(error_type)

    # Définir la taille minimale de la fenêtre
    window.minsize(200, 10)

    # Centrer la fenêtre sur l'écran
    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())

    # Définir une icône pour la fenêtre
    # window.iconbitmap('icon.ico')


    # Ajouter un label avec un message
    label = tk.Label(window, text=error_message)
    label.pack(pady=20)
    width = label.winfo_reqwidth()
    window.geometry(f"{width}x{window.winfo_reqheight()}")
    # Afficher la fenêtre
    window.mainloop()
