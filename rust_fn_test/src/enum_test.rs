#[derive(Copy, Clone, Eq, PartialEq)]
pub enum Pokemans {
    Pikachu = 25,
    Vaporeon = 134,
    Jolteon = 135,
    Flareon = 136,
    Mew = 151,
    Espeon = 196,
    Umbreon = 197,
    Girafarig = 203,
    Skitty = 300,
    Delcatty = 301,
    Drampa = 780,
}

impl Pokemans {
    pub fn is_best(&self) -> bool {
        true
    }

    pub fn is_kitty(&self) -> bool {
        match self {
            Pokemans::Mew | Pokemans::Espeon | Pokemans::Skitty | Pokemans::Delcatty => true,
            _ => false,
        }
    }

    pub fn is_giraffe(&self) -> bool {
        *self == Pokemans::Girafarig
    }

    pub fn generation(&self) -> u32 {
        match *self as u32 {
            0..=151 => 1,
            152..=251 => 2,
            252..=386 => 3,
            387..=493 => 4,
            494..=649 => 5,
            650..=721 => 6,
            722..=810 => 7,
            _ => 8,
        }
    }
}

#[test]
fn test_everything() {
    // Mostly to lazily silence dead code warnings

    let pikachu = Pokemans::Pikachu;
    let vaporeon = Pokemans::Vaporeon;
    let jolteon = Pokemans::Jolteon;
    let flareon = Pokemans::Flareon;
    let mew = Pokemans::Mew;
    let espeon = Pokemans::Espeon;
    let umbreon = Pokemans::Umbreon;
    let girafarig = Pokemans::Girafarig;
    let skitty = Pokemans::Skitty;
    let delcatty = Pokemans::Delcatty;
    let drampa = Pokemans::Drampa;

    assert_eq!(umbreon.is_kitty(), flareon.is_kitty());
    assert!(mew.generation() == 1);
    assert!(espeon.is_best() & vaporeon.is_best() & drampa.is_best());
    assert!(girafarig.is_giraffe());
    assert!(pikachu.generation() == jolteon.generation());
    assert_eq!(skitty.is_kitty(), delcatty.is_kitty());

    // Edit...that didn't silence warnings!
}
