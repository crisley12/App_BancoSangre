from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
<RootAdmin>
# <DrawerClickableItem@MDNavigationDrawerItem>
#     text_color: "#4a4939"
#     icon_color: "#4a4939"
#     ripple_color: "#FAFAFA"
#     selected_color: "#F41F05"
MDScreen:
    MDNavigationLayout:
        id: nav_layout

        MDScreenManager:
            MDScreen:
                BoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Dashboard"
                        elevation: 4
                        pos_hint: {"top": 1}
                        md_bg_color: "#F41F05"
                        specific_text_color: "#ffffff"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                    MDScreenManager:
                        id: screen_manager
                        MDScreen:
                            id: buscar_paciente
                            name: "buscar_paciente"
                            text: "Buscar Paciente"
                        MDScreen:
                            id: dashboard
                            name: "dashboard"
                        MDScreen:
                            id: registro
                            name: "registro"
                        MDScreen:
                            id: cita
                            name: "cita"
                            text: "Cita"
                        MDScreen:
                            id: logout
                            name: "logout"

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            md_bg_color: "#ffffff"

            BoxLayout:
                orientation: 'vertical'
                padding: "8dp"
                spacing: "8dp"
                ScrollView:

                MDList:
                    OneLineIconListItem:
                        text: "Buscar Paciente"
                        on_release:
                            root.screen_manager.current = "buscar_paciente"
                            nav_drawer.set_state()
                        IconLeftWidget:
                            icon: "account-search-outline"
                    
                    OneLineIconListItem:
                        text: "Cita"
                        # Aquí va lo que queremos ejecutar cuando se suelta el botón
                        on_release:
                            root.screen_manager.current = "cita"
                            nav_drawer.set_state()
                        IconLeftWidget:
                            icon: "account-search-outline"

        #     MDNavigationDrawerMenu:

        #         MDNavigationDrawerHeader:
        #             title: "Banco de Sangre"
        #             title_color: "#F41F05"
        #             text: "Basantranfs"
        #             source: "asset/img/logo_blanci.png"
        #             spacing: "4dp"
        #             padding: "12dp", 0, 0, "12dp"

        #         MDNavigationDrawerDivider:
                
        #         DrawerClickableItem:
        #             name: "user_admin"
        #             icon: "gmail"
        #             text: "Inbox"
        #             on_press:
        #                 root.nav_drawer.set_state("close")
        #                 root.screen_manager.current = "user_admin"


        #         DrawerClickableItem:
        #             name: "paciente_admin"
        #             icon: "send"
        #             text: "Outbox"
        #             on_press:
        #                 root.nav_drawer.set_state("close")
        #                 root.screen_manager.current = "paciente_admin"

        # MDNavigationLayout:
        #     MDScreenManager:
        #         id: screen_manager
        #         MDScreen:
        #             name: 'user_admin'
        #             MDLabel:
        #                 text: "hola"
        #                 halign: "center"
        #         MDScreen:
        #             name: 'paciente_admin'
        #             MDLabel:
        #                 text: "hello"
        #                 halign: "center"


'''

class RootAdmin(MDApp):
    def build(self):
        return Builder.load_string(KV)
        


RootAdmin().run()