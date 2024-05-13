from cx_Freeze import setup, Executable

buildOptions = {
	"packages":[
    	'matplotlib.pyplot','seaborn','urllib.request','json','datetime','numpy','pandas'
    ],
    "excludes":[
    
    ]
}
 
exe = [Executable('naverShoppingSc.py')]
 
setup(
    name='main',
    version='1.0',
    author='me',
    options = dict(build_exe = buildOptions),
    executables = exe
)