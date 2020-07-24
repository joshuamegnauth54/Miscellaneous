pub mod months {
    pub enum Month {
        January = 1,
        February,
        March,
        April,
        May,
        June,
        July,
        August,
        September,
        October,
        November,
        December,
    }

    pub impl Month {
        pub fn is_winter(&self) -> bool {
            match self {
                January => true,
                February => true,
                December => true,
                _ => false,
            }
        }
    }
}
