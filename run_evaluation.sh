# Generate Files
if [ $# -eq 0 ]
  then
    echo "Lauching Version without Parameters:"
    echo python3 ./evaluation_generator.py
    python3 ./evaluation_generator.py
else
    echo $#
    echo "Lauching Version with Parameters: " "$@"
    echo python3 ./evaluation_generator.py "$@"
    python3 ./evaluation_generator.py "$@"
fi

# Run experiments
python3 ./evaluation/run_all.py

