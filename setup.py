from distutils.core import setup

setup(
    name="querido-diario-toolbox",
    description="Querido Diário Toolbox",
    long_description=(
        "The goal of the `querido-diario-toolbox` is give the Querido Diário"
        "community the building blocks to perform its own analyses and manipulation in"
        "the data extracted by the Querido Diário project.  The lib should empowers the"
        "production applications used by the Querido Diário project to process the data"
        "as well as any other people which wants to perform their own analyses and"
        "run scripts."
    ),
    packages=[
        "queridodiario_toolbox",
        "queridodiario_toolbox.api",
        "queridodiario_toolbox.etl",
        "queridodiario_toolbox.process",
    ],
    url="https://github.com/okfn-brasil/querido-diario-toolbox",
)
