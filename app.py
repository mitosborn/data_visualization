import dash
import dash_bootstrap_components as dbc
#from OpenSSL import SSL

# #SSL certificates
# context = SSL.Context(SSL.metho)
# context.use_privatekey_file('server.key')
# context.use_certificate_file('server.crt')

app = dash.Dash(__name__, title="TX Covid-19 Enviro-Map",
                suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX])
# app.scripts.append_script({‘external_url’:‘https://mywebsite.com/assets/gtag.js’})

app.index_string = '''<!DOCTYPE html>
<html>
    <head>
    {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-N6T2RXG');</script>
    </head>
    <body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=G-C2CZEJ5N67"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

server = app.server
