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

fn main() {
    println!("The absolute value of -32 is {}.", abs(-32.0));

    let numbers = vec![14.0, 28.0, 42.0];
    println!("Mean: {}", mean(&numbers));
    println!("Variance: {}", var(&numbers));
}
