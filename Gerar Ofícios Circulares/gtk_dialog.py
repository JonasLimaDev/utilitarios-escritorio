import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def open_file_dialog(type_file_filter={},titulo="Selecione o Arquivo"):
    dialog = Gtk.FileChooserDialog(title=titulo,  action=Gtk.FileChooserAction.OPEN)
    dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.OK,
    )
    ## filtros de arquivos
    if type_file_filter:
        for tipo_filtro in type_file_filter.keys():
            filtro = Gtk.FileFilter()
            filtro.set_name(tipo_filtro)
            filtro.add_mime_type(type_file_filter[tipo_filtro])
            dialog.add_filter(filtro)
    
    filter_any = Gtk.FileFilter()
    filter_any.set_name("Todos Arquivos")
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)
    ######
    
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        return dialog.get_filename()
    elif response == Gtk.ResponseType.CANCEL:
        #print("Cancel clicked")
        return None
            
    dialog.destroy()


if __name__ == '__main__':
    arquivo = open_file_dialog()

