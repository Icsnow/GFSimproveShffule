@echo off

echo "Start GFS_pi evaluation!"
echo "========================"
timeout /nobreak /t 2 >nul


cd C:\Users\Snow\Nutstore\1\Improve_Shuffle_in_GFS\DrawingPaper\FileUpdate\GFSimproveShffule\shuffleEvaluation

:: echo "Call _diffusion.py ..."
:: call python _diffusion.py
:: echo "Evaluation of **diffusion property** is finished !"
:: echo "========================"

:: echo "Call _DS_MITM.py ..."
:: call python _DS_MITM.py
:: echo "Evaluation of **DS-MITM** is finished !"
:: echo "========================"

:: echo "Call _impossible_differential.py ..."
:: call python _impossible_differential.py
:: echo "Evaluation of **impossible differential** is finished !"
:: echo "========================"

echo "Call _zc_linear.py ..."
call python _zc_linear.py
echo "Evaluation of **zero-correlated linear** is finished !"
echo "========================"

echo "Call _differential.py ..."
call python _differential.py
echo "Evaluation of **differential** is finished !"
echo "========================"

echo "Call _linear.py ..."
call python _linear.py
echo "Evaluation of **linear** is finished !"
echo "========================"

echo "Call _division_property.py ..."
call python _division_property.py
echo "Evaluation of **division property** is finished !"
echo "========================"

timeout /nobreak /t 2 >nul
echo "Evaluation are all Finished"

pause