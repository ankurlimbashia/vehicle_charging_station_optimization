mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"ankurlimbashia12@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
base=\"dark\"\n\

" > ~/.streamlit/config.toml