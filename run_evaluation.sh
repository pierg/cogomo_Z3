# Generate Files
if [ $# -eq 0 ]
  then
    python3 ./evaluation_generator.py
else
    python3 ./evaluation_generator.py "$@"
fi

# Run experiments
python3 ./evaluation/run_all.py

