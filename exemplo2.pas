{# Exemplo 2: Programa com IF e WHILE #}

program exemplo_controle;
var
  i, soma, n : integer;

begin
  n := 10;
  soma := 0;
  i := 1;
  
  while i < n do
  begin
    if i > 5 then
      soma := soma + i
    else
      soma := soma + 1;
    i := i + 1;
  end;
  
  write(soma);
end.
