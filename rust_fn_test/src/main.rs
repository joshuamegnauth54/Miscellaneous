use rand::thread_rng;
use rand_distr::{Distribution, Normal};
use std::vec::Vec;

fn abs(number: f64) -> f64 {
    if number >= 0.0 {
        number
    } else {
        -number
    }
}

fn mean(numbers: &Vec<f64>) -> f64 {
    numbers.iter().sum::<f64>() / numbers.len() as f64
}

fn var(numbers: &Vec<f64>) -> f64 {
    let mean = mean(numbers);
    let mut var_tmp = numbers.clone();

    for num in var_tmp.iter_mut() {
        *num = (*num - mean).powi(2);
    }

    var_tmp.iter().sum::<f64>() / var_tmp.len() as f64 - 1.0
}

fn std(numbers: &Vec<f64>) -> f64 {
    var(numbers).sqrt()
}

fn factorial(n: u64) -> u64 {
    if n == 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}

fn main() {
    let rng = thread_rng();
    println!("The absolute value of -32 is {}.", abs(-32.0));

    let numbers = vec![14.0, 28.0, 42.0];
    println!("Mean: {}", mean(&numbers));
    println!("Variance: {} Std. Dev.: {}", var(&numbers), std(&numbers));
    println!("10!: {}", factorial(10));
}
