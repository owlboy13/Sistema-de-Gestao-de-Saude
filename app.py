
from patients import Patients
from patients import view_statistics, find_patient, list_patients, del_patient


class App:

    def __init__(self):
        pass

    def menu(self):
        while True:
            try:
                print("\n===SISTEMA CLÍNICA VIDA+===")
                options = int(input("""
                        \n1. Cadastrar Paciente
                        \n2. Ver Estatísticas
                        \n3. Buscar paciente
                        \n4. Listar todos os pacientes
                        \n5. Deletar Paciente
                        \n6. Sair
                        \nEscolha uma opção: """))

                comands_ = {
                        1: lambda: Patients(
                            name=str(
                                input("Digite o nome completo do paciente: ")),
                            age=int(
                                input("Digite a idade do paciente: ")),
                            phone=str(
                                input("Digite o número de telefone do "
                                      "paciente com DDD: "))).register(),
                        2: lambda: view_statistics(),
                        3: lambda: find_patient(),
                        4: lambda: list_patients(),
                        5: lambda: del_patient()
                    }
                if options in comands_:
                    menu_comands = comands_[options]

                elif options == 5:
                    print("\nDesconectando...")
                    break

                else:
                    print("\nComando Inexistente, tente novamente...")

                menu_comands()

            except TypeError:
                print("Erro no tipo de comando,"
                      "digite números para escolher a opção")


if __name__ == '__main__':
    app = App()
    app.menu()
