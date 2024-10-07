![[Pasted image 20241002101258.png]]


formatter: function (value) {
                var date = new Date(value);
                var day = date.getDate();
                var month = date.getMonth() + 1;
                var year = date.getFullYear();

                // Проверяем, является ли день первым или последним днем месяца
                if (day === 1 || day === new Date(year, month, 0).getDate()) {
                    return `${day}.${month}.${year}`;
                } else {
                    return '';
                }
            }