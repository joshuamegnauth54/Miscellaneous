use std::vec::Vec;

pub fn abs(number: f64) -> f64 {
    if number >= 0.0 {
        number
    } else {
        -number
    }
}

pub fn mean(numbers: &Vec<f64>) -> f64 {
    numbers.iter().sum::<f64>() / numbers.len() as f64
}

pub fn var(numbers: &Vec<f64>) -> f64 {
    let mean = mean(numbers);
    let mut var_tmp = numbers.clone();

    for num in var_tmp.iter_mut() {
        *num = (*num - mean).powi(2);
    }

    var_tmp.iter().sum::<f64>() / var_tmp.len() as f64 - 1.0
}

pub fn std(numbers: &Vec<f64>) -> f64 {
    var(numbers).sqrt()
}

pub fn factorial(n: u64) -> u64 {
    if n == 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}
