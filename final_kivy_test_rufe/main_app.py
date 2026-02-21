from kivy.app import App  

from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


from kivy.core.window import Window

from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits
from ruffier import test, ruffier_index

from seconds import Seconds
from sits import Sits
from runner import Runner

Window.clearcolor = (0.6, 0.5, 1, 0.33)

age = 7

name = ""

def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        instruction = Label(text = txt_instruction)
        
        name_text = Label(text = "Введіть ім'я:", halign = "right")
        self.in_name = TextInput(multiline=False)

        age_text = Label(text = "Введіть вік:", halign = "right")
        self.in_age = TextInput(text="7", multiline=False)

        self.button = Button(text="Почати", size_hint=(0.3, 0.1), pos_hint = {"center_x": 0.5})
        self.button.on_press = self.next
        
        self.button_exit = Button(text="Вихід", size_hint=(0.3, 0.1), pos_hint = {"center_x": 0.5})
        self.button_exit.on_press = App.get_running_app().stop

        line1 = BoxLayout(size_hint=(0.8, None), height = "30sp")
        line2 = BoxLayout(size_hint=(0.8, None), height = "30sp")

        line1.add_widget(name_text)
        line1.add_widget(self.in_name)

        line2.add_widget(age_text)
        line2.add_widget(self.in_age)

        main_line = BoxLayout(orientation = "vertical", padding = 8, spacing = 8)
        main_line.add_widget(instruction)
        main_line.add_widget(line1)
        main_line.add_widget(line2)
        main_line.add_widget(self.button)
        main_line.add_widget(self.button_exit)
        
        self.add_widget(main_line)

    def next(self):
        global name, age
        name = self.in_name.text
        age = check_int(self.in_age.text)
        if age == False or age < 7:
            age = 7
            self.in_age.text = str(age)
        else:
            self.manager.current = "take_pulse1"



class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        
        instr = Label(text=txt_test1)
        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done=self.sec_finished)

        line = BoxLayout(size_hint=(0.8, None), height='30sp')
        lbl_result = Label(text='Введіть результат:', halign='right')
        self.in_result = TextInput(text='0', multiline=False)
        self.in_result.set_disabled(True)
        
        line.add_widget(lbl_result)
        line.add_widget(self.in_result)
    
        self.btn = Button(text='Почати', pos_hint={'center_x': 0.5})
        self.btn.on_press = self.next
        
        self.btn_exit = Button(text='Вихід', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        self.btn_exit.on_press = App.get_running_app().stop
    
        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(self.lbl_sec)
        outer.add_widget(line)
        self.line3 = BoxLayout(size_hint=(0.8, None), height='80sp', pos_hint={'center_x': 0.5})
        self.line3.add_widget(self.btn)
        outer.add_widget(self.line3)
        outer.add_widget(self.btn_exit)
        
        self.add_widget(outer)

    def sec_finished(self, *args):
        self.next_screen = True
        self.in_result.set_disabled(False)
        self.btn.set_disabled(False)
        self.btn.text = 'Продовжити'

        self.line3.remove_widget(self.btn)
        self.line3.add_widget(self.btn)

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.lbl_sec.start()
        else:
            global p1
            p1 = check_int(self.in_result.text)
            if p1 == False or p1 <= 0:
                p1 = 0
                self.in_result.text = str(p1)
            else:
                self.manager.current = 'sits'

class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False

        instr = Label(text=txt_sits, size_hint=(0.5, 1))
        self.lbl_sits = Sits(30)
        self.run = Runner(total=30, steptime=1.5, size_hint=(0.4, 1))
        self.run.bind(finished=self.run_finished)

        line = BoxLayout()
        vlay = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        vlay.add_widget(self.lbl_sits)
        line.add_widget(instr)
        line.add_widget(vlay)
        line.add_widget(self.run)

        self.btn = Button(text='Почати', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn.on_press = self.next
        
        self.btn_exit = Button(text='Вихід', size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        self.btn_exit.on_press = App.get_running_app().stop

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(line)
        outer.add_widget(self.btn)
        outer.add_widget(self.btn_exit)

        self.add_widget(outer)

    def run_finished(self, instance, value):
        self.btn.set_disabled(False)
        self.btn.text = 'Продовжити'
        self.next_screen = True

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.run.start()
            self.run.bind(value=self.lbl_sits.next)
        else:
            self.manager.current = 'take_pulse2'

class FourthScreen(Screen):
    def __init__(self, **kwargs):
        self.next_screen = False

        self.stage = 0
        super().__init__(**kwargs)

        instr = Label(text=txt_test3)

        line1 = BoxLayout(size_hint=(0.8, None), height="30sp")
        self.label_seconds = Seconds(15)
        self.label_seconds.bind(done=self.sec_finished)
        self.label1 = Label(text="Рахуйте пульс")

        label_result1 = Label(text="Результат:", halign="right")
        self.in_result1 = TextInput(text="0", multiline=False)

        line1.add_widget(label_result1)
        line1.add_widget(self.in_result1)


        line2 = BoxLayout(size_hint=(0.8, None), height="30sp")
        label_result2 = Label(text="Результати після відпочинку:", halign="right")
        self.in_result2 = TextInput(text="0", multiline=False)

        self.in_result1.set_disabled(True)
        self.in_result2.set_disabled(True)

        line2.add_widget(label_result2)
        line2.add_widget(self.in_result2)

        self.button = Button(text="Почати", size_hint=(0.3, 0.5), pos_hint={"center_x":0.5})
        self.button.on_press = self.next
        
        self.button_exit = Button(text="Вихід", size_hint=(0.3, 0.1), pos_hint={"center_x": 0.5})
        self.button_exit.on_press = App.get_running_app().stop

        main_line = BoxLayout(orientation = "vertical", padding=8, spacing=8)
        main_line.add_widget(instr)
        main_line.add_widget(self.label1)
        main_line.add_widget(self.label_seconds)
        main_line.add_widget(line1)
        main_line.add_widget(line2)
        main_line.add_widget(self.button)
        main_line.add_widget(self.button_exit)

        self.add_widget(main_line)


    def sec_finished(self, *args):
        if self.label_seconds.done:
            if self.stage == 0:
                self.stage = 1
                self.label1.text = 'Відпочивайте'
                self.label_seconds.restart(30)
                self.in_result1.set_disabled(False)
            elif self.stage == 1:
                self.stage = 2
                self.label1.text='Рахуйте пульс'
                self.label_seconds.restart(15)
            elif self.stage == 2:
                self.in_result2.set_disabled(False)
                self.button.set_disabled(False)
                self.button.text = 'Завершити'
                self.next_screen = True
 
    def next(self):
        if not self.next_screen:
                self.button.set_disabled(True)
                self.label_seconds.start()
        else:
                global p2, p3
                p2 = check_int(self.in_result1.text)
                p3 = check_int(self.in_result2.text)
                if p2 == False:
                    p2 = 0
                    self.in_result1.text = str(p2)
                elif p3 == False:
                    p3 = 0
                    self.in_result2.text = str(p3)
                else:
                    self.manager.current = 'result'

class FifthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.instr = Label(text = '')
        self.outer.add_widget(self.instr)
    
        self.btn_exit = Button(text="Вихід", size_hint=(0.3, 0.1), pos_hint={"center_x": 0.5})
        self.btn_exit.on_press = App.get_running_app().stop
        
        self.outer.add_widget(self.btn_exit)
        self.add_widget(self.outer)
        self.on_enter = self.before
  
    def before(self):
        global name
        self.instr.text = name + '\n' + test(p1, p2, p3, age)

class RunningApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name = "instruction"))
        sm.add_widget(SecondScreen(name = "take_pulse1"))
        sm.add_widget(ThirdScreen(name = "sits"))
        sm.add_widget(FourthScreen(name = "take_pulse2"))
        sm.add_widget(FifthScreen(name="result"))
        return sm
    
app = RunningApp()
app.run()