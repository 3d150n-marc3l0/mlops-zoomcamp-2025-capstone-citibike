import yaml



with open('configs/zenml/training_pipeline.local.yaml', 'r') as file:
    prime_service = yaml.safe_load(file)
    print(prime_service)
    print(prime_service['parameters']['n_trials'])

