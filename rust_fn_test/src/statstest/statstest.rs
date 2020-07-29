use std::vec::Vec;

pub fn abs(number: f64) -> f64 {
    if number >= 0.0 {
        number
    } else {
        -number
    }
}

pub fn mean(numbers: &[f64]) -> f64 {
    numbers.iter().sum::<f64>() / numbers.len() as f64
}

pub fn var(numbers: &[f64]) -> f64 {
    let mean = mean(numbers);
    let mut var_tmp = numbers.to_vec();

    for num in var_tmp.iter_mut() {
        *num = (*num - mean).powi(2);
    }

    var_tmp.iter().sum::<f64>() / var_tmp.len() as f64 - 1.0
}

pub fn std(numbers: &[f64]) -> f64 {
    var(numbers).sqrt()
}

pub fn standardize(numbers: &[f64]) -> Vec<f64> {
    let mut temp = numbers.to_vec();
    let mean = mean(numbers);
    let std = std(numbers);

    for val in temp.iter_mut() {
        *val = (*val - mean) / std;
    }

    temp
}

pub fn factorial(n: u64) -> u64 {
    if n == 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}
