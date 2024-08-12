echo "cleaning CIRCUITPY"
for entry in /media/$USER/CIRCUITPY/*
do 
    case $entry in
        *.py)
        #*.py | *.pcf)
            echo "rm" $entry
            rm $entry
            ;;
    esac
done

echo 

echo "uploading new firmware"
for entry in *
do
    case $entry in 
        *.py)
        #*.py |*.pcf)
            echo $entry "->" /media/$USER/CIRCUITPY
            cp $entry /media/$USER/CIRCUITPY
            ;;
    esac
done
sync
