from bowtie.visual import Plotly, Markdown
from bowtie.control import Nouislider, Upload, Dropdown, Slider, Button, Textbox
from Analyzer.ResultAnalizer import ResultAnalyzer
from main import run_experiment
from utils.utils import *


sine_plot = Plotly()
freq_slider = Nouislider(caption='Aggregation time, ms', minimum=50, maximum=2000, start=500)
upload = Upload(multiple=False, caption='Upload json config')
run_button = Button(label="Run the experiment!")
dropdown_src = Dropdown(caption='src_ips', labels=[''], values=[''])
dropdown_dst = Dropdown(caption='dst_ips', labels=[''], values=[''])
scale_factor_input = Nouislider(caption='Scaling factor', start=1, minimum=0, maximum=1)
mark = Markdown(u'NNN')

#text = Textbox(area=True, autosize=True, placeholder='Enter markdown')


result_analyzer = ResultAnalyzer()
src_ips = []
dst_ips = []
initialized = False
config = None
config_valid = False

def upload_listener(name, file):
    #result_analyzer.read_df(file)
    global config_valid
    global config

    print("UPLOADING", name, file)

    config = read_json(name)
    print("CONFIG READ")
    print("Config = ", config)

    validation_text = validate_config(config)
    print("valudation text", validation_text)
    if validation_text:
        print("CONFIG IS NOT VALID")
        print(validation_text)
        config_valid = False
    else:
        config_valid = True


def update_scale_factor(scale_factor):
    scale_factor = float(scale_factor[0])
    result_analyzer.scale_factor_ = scale_factor
    freq = freq_slider.get()
    slider_listener([freq])


def dropdown_src_listener(f1):
    global src_ips
    global dst_ips

    value = f1['value']
    if value == '':
        src_ips = []
    else:
        src_ips = [f1['value']]

    dst_ips = result_analyzer.get_src_ip(src_ips)
    dropdown_dst.do_options(labels=[""] + dst_ips, values=[""] + dst_ips)

    freq = freq_slider.get()
    slider_listener([freq])


def button_listener():
    scale_factor = float(scale_factor_input.get())
    print("SCALE_FACTOR = ", scale_factor)
    sine_plot.progress.do_percent(0)
    sine_plot.progress.do_visible(True)
    run_experiment(config, scale_factor)
    sine_plot.progress.do_percent(100)
    sine_plot.progress.do_visible(False)

    result_analyzer.read_df(config)
    print("")

def dropdown_dst_listener(f1):
    global dst_ips
    global src_ips

    value = f1['value']
    if value == '':
        dst_ips = []
    else:
        dst_ips = [f1['value']]

    freq = freq_slider.get()
    slider_listener([freq])


def slider_listener(freq):
    global src_ips
    global dst_ips
    global initialized

    if not initialized:
        src_ips = result_analyzer.get_src_ip()
        dst_ips = result_analyzer.get_src_ip()
        dropdown_src.do_options(labels=[""] + src_ips, values=[""] + src_ips)
        dropdown_dst.do_options(labels=[""] + dst_ips, values=[""] + dst_ips)
        initialized = True

    freq = int(float(freq[0]))
    freq = str(freq) + 'ms'

    x, y = result_analyzer.calc_xy(freq, ip_srcs=src_ips, ip_dsts=dst_ips)

    sine_plot.do_all({
        'data': [{
            'type': 'scatter',
            'mode': 'lines',
            'x': x,
            'y': y
        }],
        'layout': {
            'title': 'Traffic',
            'yaxis':{'title': 'Mbit'},
            'xaxis': {'title': 'seconds'},
        }
    })


def write(txt):
    print(txt)
    print(type(txt))
    mark.do_text(txt)

from bowtie import command
@command
def main():
    from bowtie import App
    app = App(title='Network DownScaler')

    app.add(sine_plot)

    app.add_sidebar(upload)
    app.subscribe(upload_listener, upload.on_upload)

    app.add_sidebar(scale_factor_input)
    app.subscribe(update_scale_factor, scale_factor_input.on_change)

    app.add_sidebar(mark)

    #app.add_sidebar(text)
    #app.subscribe(write, text.on_change)

    app.add_sidebar(run_button)
    app.subscribe(button_listener, run_button.on_click)

    app.add_sidebar(freq_slider)
    app.subscribe(slider_listener, freq_slider.on_change)

    app.add_sidebar(dropdown_src)
    app.add_sidebar(dropdown_dst)

    app.subscribe(dropdown_src_listener, dropdown_src.on_change)
    app.subscribe(dropdown_dst_listener, dropdown_dst.on_change)


    return app
