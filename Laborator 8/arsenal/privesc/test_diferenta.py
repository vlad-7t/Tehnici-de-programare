def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b"}
    a= ["f,f,ds,f,s,"]
    assert acum - baza == {"c"}
