from bowtie.visual import Plotly
from bowtie.control import Nouislider, Upload, Dropdown
from Analizer.ResultAnalizer import ResultAnalyzer
import plotlywrapper as pw


sine_plot = Plotly()
freq_slider = Nouislider(caption='Aggregation time, ms', minimum=50, maximum=2000, start=500)
upload = Upload(multiple=False, caption='Upload csv to analyze')
dropdown_src = Dropdown(caption='src_ips', labels=[''], values=[''])
dropdown_dst = Dropdown(caption='dst_ips', labels=[''], values=[''])

result_analyzer = ResultAnalyzer()
src_ips = []
dst_ips = []
initialized = False

def upload_listener(name, file):
    result_analyzer.read_df(file)

def iniitalize_dropdown():
    result_analyzer.get_dst_ip()

def dropdown_src_listener(f1):
    global src_ips
    global dst_ips

    value = f1['value']
    if value == '':
        src_ips = []
    else:
        src_ips = [f1['value']]

    print("DROPDOWN SRC UPDATE = ", f1)

    dst_ips = result_analyzer.get_src_ip(src_ips)
    dropdown_dst.do_options(labels=[""] + dst_ips, values=[""] + dst_ips)

    freq = freq_slider.get()
    slider_listener([freq])


def dropdown_dst_listener(f1):
    global dst_ips
    global src_ips

    value = f1['value']
    if value == '':
        dst_ips = []
    else:
        dst_ips = [f1['value']]

    print("DROPDOWN DST UPDATE = ", f1)

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

    print('src ip = ' , src_ips, dst_ips, freq)

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
            'title': 'TITLE',
            'yaxis':{'title': 'Mbit'},
            'xaxis': {'title': 'seconds'},
        }
    })


#fig = go.Figure(data=data, layout=layout)

from bowtie import command
@command
def main():
    from bowtie import App
    app = App(title='Network DownScaler')

    app.add(sine_plot)

    app.add_sidebar(upload)
    app.subscribe(upload_listener, upload.on_upload)

    app.add_sidebar(freq_slider)
    app.subscribe(slider_listener, freq_slider.on_change)

    app.add_sidebar(dropdown_src)
    app.add_sidebar(dropdown_dst)

    app.subscribe(dropdown_src_listener, dropdown_src.on_change)
    app.subscribe(dropdown_dst_listener, dropdown_dst.on_change)

    return app
