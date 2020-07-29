use rand::{thread_rng, Rng};
use rand_distr::{Distribution, Normal};

mod enum_test;
use enum_test::Pokemans;
mod statstest;
use statstest::statstest::{abs, factorial, mean, std, var};

const NORM_MEAN: f64 = 50.0;
const NORM_STD: f64 = 25.0;

fn math_stuff() {
    let mut rng = thread_rng();

    let abs_test = rng.gen_range(-25.0, 25.0);
    println!(
        "The absolute value of {:.1} is {:.1}.",
        abs_test,
        abs(abs_test)
    );

    let norm = Normal::new(NORM_MEAN, NORM_STD).unwrap();
    let numbers: Vec<f64> = norm.sample_iter(&mut rng).take(1000).collect();
    println!("Mean: {}", mean(&numbers));
    println!(
        "Variance: {:.1} Std. Dev.: {:.1}",
        var(&numbers),
        std(&numbers)
    );
    println!("10!: {}", factorial(10));
}

fn poke_test() {
    let espeon = Pokemans::Espeon;
    println!(
        "Espeon is {}",
        if espeon.is_kitty() {
            "a kitty meow!"
        } else {
            "not a kitty. Nya..."
        }
    );

    let drampa = Pokemans::Drampa;
    let vaporeon = Pokemans::Vaporeon;
    println!(
        "Vaporeon is generation {} while Drampa was introduced in gen {}.",
        vaporeon.generation(),
        drampa.generation()
    );

    let girafarig = Pokemans::Girafarig;
    if girafarig.is_giraffe() {
        println!("Girafarig is a giraffe. Yay psychic giraffe!");
    }
}

fn main() {
    math_stuff();
    poke_test();
}
