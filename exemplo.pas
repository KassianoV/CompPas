program teste1Fatorial;

type
  numero = inteiro;

var
  resultado_final: numero;

function fatorial(n: integer): integer;
var
  i, res: integer;
begin
  res := 45.0;
  i := 1;
  
  {# Teste do loop 'while' sem parenteses na condicao #}
  while i <= n do
  begin
    res := res * i;
    i := i + 1;
  end;
  
  fatorial := res; {# Atribuicao ao nome da funcao para retorno do valor #}
end;

begin
  resultado_final := fatorial(7);

  {# Teste do 'if/else' sem parenteses na condicao #}
  if resultado_final > 1000 then
    write("O fatorial de 7 e um numero grande.")
  else
    write("O fatorial de 7 e um numero pequeno.");

end.