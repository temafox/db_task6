import vet_ui as ui
import vet_cmd as cmd

def main():
    ui.show("greeting")

    while True:
        ui.show("prompt")
        try:
            command = cmd.receive()
        except Exception as ex:
            print("Exception:", ex)
            continue

        if cmd.is_exit(command):
            break
        elif not cmd.is_empty(command):
            cmd.execute(command)

if __name__ == '__main__':
    main()
