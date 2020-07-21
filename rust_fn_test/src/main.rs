use rand::{thread_rng, Rng};
use rand_distr::{Distribution, Normal};
use std::vec::Vec;

const NORM_MEAN: f64 = 50.0;
const NORM_STD: f64 = 25.0;

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
    let mut rng = thread_rng();

    let abs_test = rng.gen_range(-25.0, 25.0);
    println!(
        "The absolute value of {:.1} is {:.1}.",
        abs_test,
        abs(abs_test)
    );

    let norm = Normal::new(NORM_MEAN, NORM_STD).unwrap();
    let numbers = norm.sample_iter(&mut rng).take(1000).collect();
    println!("Mean: {}", mean(&numbers));
    println!(
        "Variance: {:.1} Std. Dev.: {:.1}",
        var(&numbers),
        std(&numbers)
    );
    println!("10!: {}", factorial(10));
}
