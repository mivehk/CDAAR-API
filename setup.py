from setuptools import setup

setup(
    name="cdaar",
    version="2.0.1",
    description="RESTful API for the central dogma of molecular biology",
    author="Kayvan Mivehnejad",
    url="https://dev15.miveh-nejad.info",
    py_modules=["cdaar"],
    install_requires=[
        "flask==3.1.0",
        "pydantic==2.10.6",
        "flask-openapi3==4.1.0",
        "flask-openapi3-swagger==5.20.0",
        "flask-openapi3-redoc==2.4.0",
        "flask-openapi3-rapidoc==9.3.8",
        "flask-openapi3-rapipdf==2.2.1",
        "flask-openapi3-scalar==1.25.127",
        "flask-openapi3-elements==9.0.0",
    ],
)
