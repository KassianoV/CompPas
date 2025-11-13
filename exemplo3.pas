{# Exemplo 3: Programa com função #}

program exemplo_funcao;
var
  resultado, x, y : integer;

function soma(a: integer; b: integer) : integer;
begin
  soma := a + b;
end;

function fatorial(n: integer) : integer;
var
  i, fat : integer;
begin
  fat := 1;
  i := 2;
  while i < n do
  begin
    fat := fat * i;
    i := i + 1;
  end;
  fatorial := fat;
end;

begin
  x := 5;
  y := 3;
  resultado := soma(x, y);
  write(resultado);
  
  resultado := fatorial(5);
  write(resultado);
end.
