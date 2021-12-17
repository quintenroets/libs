from libs.cli import Cli

class Gui:
    @staticmethod
    def ask(question, options=None):
        question = question.replace("'", "")
        question = f"<big>{question}</big>"
        if options is None:
            options = {"text": question}
            return Gui.run("entry", options)
        elif isinstance(options, list):
            return Gui.ask_options(question, options)
        
    @staticmethod
    def ask_yn(question):
        return Cli.get(f"kdialog --yesno '{question}' && echo confirmed", check=False)

    @staticmethod
    def ask_options(question, options):
        display_options = {o.replace("&", "").replace("'", ""): o for o in options} # remove quotes from options in command
        options_string = " ".join([f"'{o}' 'Monospace 15'" for o in display_options])
        separator = "###"
        options = {"separator": separator, "text": question, "no-headers": None}
        response = Gui.run(f"list --column=text --column=@font@ {options_string}", options)
        if response:
            response = response.split(separator)[0]
            response = display_options[response] # convert back to original option
        return response

    @staticmethod
    def run(subcommand, custom_options=None):
        options = {
            "geometry": "907x514+500+200",
            "title": "",
            "text-align": "center",
            "icon-theme": "Win11",
            "fontname": "Noto Sans 40"
        }
        options.update(custom_options)
        options = " ".join([f"--{k}" if v is None else f"--{k}='{v}'" for k, v in options.items()])
        command = f"yad {options} --{subcommand}"
        result = Cli.get(command, check=False)
        return result
