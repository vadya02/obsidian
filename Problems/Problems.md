
Problem:
TypeError: The 'compilation' argument must be an instance of Compilation
![[Pasted image 20240716111742.png]]

Решение:
все из за регистра в пути (вместо C:\Users\MandanovVM1\Desktop\superset\bi> нужно указывать C:\Users\MandanovVM1\Desktop\superset\BI>)





Условия:
node: 20 lts
![[Pasted image 20240716110744.png]]
Результат:
![[Pasted image 20240716111742.png]]




Условия:
node: 20 lts
![[Pasted image 20240716111955.png]]
Результат:
![[Pasted image 20240716113846.png]]

Условия:
node 18 lts
![[Pasted image 20240716114513.png]]

Результат:


возможно влияют права админа (делать npm install от админа)

возможно влияет регистр в пути папок (в powershell)

Решение: 
==Регистр в пути к проекту влияет на webpack==



если ругается на импорты loaders.gl и в папке handlebars, нужно удалить node_modules в папках handlebars и C:\Users\MandanovVM1\Desktop\superset\BI\superset-frontend\plugins\plugin-chart-country-map-v2. 
Также нужно удалить общий node_modules и запустить npm install.



![[Pasted image 20240731130741.png]]

Решение:
![[Pasted image 20240731130800.png]]

