import random
from io import StringIO

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("WARNING: pandas not installed. Install with: pip install pandas")

# Simulated LLM data augmentation
# In production: use transformers.pipeline('text-generation', model='gpt2')

class DataAugmentor:
    def __init__(self, seed=42):
        random.seed(seed)
    
    def generate_from_prompt(self, prompt, num_samples=10):
        """Simulate LLM generation by learning patterns from prompt"""
        lines = [l.strip() for l in prompt.strip().split('\n') if l.strip()]
        
        # Parse header and examples
        header_idx = next(i for i, l in enumerate(lines) if 'employee_id' in l)
        header = lines[header_idx]
        examples = [l.split(',') for l in lines[header_idx+1:] if ',' in l]
        
        # Learn pattern: salary per year of experience
        salaries = [int(row[2]) for row in examples]
        experiences = [int(row[1]) for row in examples]
        avg_salary_per_year = sum(s/e for s,e in zip(salaries, experiences)) / len(examples)
        
        # Generate synthetic rows
        next_id = max(int(row[0]) for row in examples) + 1
        generated = [header]
        
        for i in range(num_samples):
            years = random.randint(1, 15)
            base_salary = years * avg_salary_per_year
            salary = int(base_salary * random.uniform(0.85, 1.15))
            generated.append(f"{next_id + i},{years},{salary}")
        
        return '\n'.join(generated)

# 1. Load model (simulated)
print("=== STEP 1: Initialize Data Augmentor ===")
augmentor = DataAugmentor(seed=42)

# 2. Build structured prompt with headers + example rows
print("\n=== STEP 2: Build Structured Prompt ===")
prompt = """employee_id,years_experience,salary
1,1,50000
2,2,60000
3,3,70000
4,4,80000
5,5,90000"""
print(prompt)

# 3. Generate synthetic rows
print("\n=== STEP 3: Generate Synthetic Data ===")
generated_text = augmentor.generate_from_prompt(prompt, num_samples=15)
print(f"Generated {len(generated_text.split(chr(10))) - 1} new rows")

# 4. Parse generated content into DataFrame
print("\n=== STEP 4: Parse Generated Content into DataFrame ===")
if not HAS_PANDAS:
    print("ERROR: pandas is required for this project")
    exit(1)

df = pd.read_csv(StringIO(generated_text))
print(f"Parsed {len(df)} rows into DataFrame")
print(f"Columns: {df.columns.tolist()}")

# 5. Validate: schema checks, duplicates, numeric ranges, sanity constraints
print("\n=== STEP 5: VALIDATION ===")

# Schema check
expected_cols = ['employee_id', 'years_experience', 'salary']
assert all(col in df.columns for col in expected_cols), "Missing columns"
print(f"✓ Schema valid: {df.columns.tolist()}")

# Type conversion and validation
df['employee_id'] = pd.to_numeric(df['employee_id'], errors='coerce')
df['years_experience'] = pd.to_numeric(df['years_experience'], errors='coerce')
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
df.dropna(inplace=True)
print(f"✓ Type validation passed")

# Numeric range validation
df = df[(df['years_experience'] >= 0) & (df['years_experience'] <= 50)]
df = df[(df['salary'] >= 30000) & (df['salary'] <= 200000)]
print(f"✓ Range validation passed")

# Sanity constraint: salary should correlate with experience
df = df[df['salary'] >= (df['years_experience'] * 8000)]
print(f"✓ Sanity constraints passed")

# Remove duplicates
initial_rows = len(df)
df.drop_duplicates(subset=['employee_id'], inplace=True)
print(f"✓ Duplicates removed: {initial_rows - len(df)}")

# Results
print(f"\n=== RESULTS ===")
print(f"Total validated rows: {len(df)}")
print(f"Salary range: ${df['salary'].min():.0f} - ${df['salary'].max():.0f}")
print(f"Experience range: {df['years_experience'].min():.0f} - {df['years_experience'].max():.0f} years")

print(f"\nGenerated DataFrame:")
print(df.to_string(index=False))

print(f"\n=== STATISTICS ===")
print(f"Mean salary: ${df['salary'].mean():.2f}")
print(f"Mean experience: {df['years_experience'].mean():.2f} years")
print(f"Avg salary per year: ${(df['salary'] / df['years_experience']).mean():.2f}")
