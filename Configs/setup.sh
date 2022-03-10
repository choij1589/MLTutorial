### setup.sh
### tamsa 1/2 are not sharing home directory. Let's use /data6/Users/$USER/MLTutorial/.local as python user base
export TUTORIAL_BASE="/data6/Users/$USER/MLTutorial"
export PYTHONUSERBASE=${TUTORIAL_BASE}/.local

### Most of the ML tools can be used by LCG_101cuda
### Set up CUDA, CUDNN, python, root...
source /cvmfs/sft.cern.ch/lcg/releases/LCG_101cuda/cuda/11.2/x86_64-centos7-gcc8-opt/setup.sh
source /cvmfs/sft.cern.ch/lcg/releases/LCG_101cuda/cudnn/8.1.1.33/x86_64-centos7-gcc8-opt/cudnn-env.sh
source /cvmfs/sft.cern.ch/lcg/releases/LCG_101cuda/Python/3.8.6/x86_64-centos7-gcc8-opt/Python-env.sh
source /cvmfs/sft.cern.ch/lcg/releases/LCG_101cuda/xgboost/0.90/x86_64-centos7-gcc8-opt/xgboost-env.sh
source /cvmfs/sft.cern.ch/lcg/releases/LCG_101cuda/matplotlib/3.4.3/x86_64-centos7-gcc8-opt/matplotlib-env.sh
source /cvmfs/sft.cern.ch/lcg/releases/LCG_101cuda/blas/0.3.17.openblas/x86_64-centos7-gcc8-opt/blas-env.sh
source /cvmfs/sft.cern.ch/lcg/releases/LCG_101cuda/tbb/2020_U2/x86_64-centos7-gcc8-opt/tbb-env.sh
source /cvmfs/sft.cern.ch/lcg/releases/LCG_101cuda/ROOT/6.24.06/x86_64-centos7-gcc8-opt/bin/thisroot.sh
