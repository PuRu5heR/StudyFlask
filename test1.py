from jinja2 import Template


names = ["user1", "user2", "user3", "user4", "user5", "user6"]
ages = [10, 15, 18, 26, 56, 16]

table = """<table border>
                <tr>
                    <td>Имя</td>
                    <td>Возраст</td>
                    <td>Статус</td>
                </tr>
                {% for i in range(length_list) -%}
                <tr>
                    <td>{{names[i]}}</td>
                    <td>{{ages[i]}}</td>
                    {% if ages[i] < 18 -%}
                        <td>Несовершеннолетний</td>
                    {% else -%}
                        <td>Совершеннолетний</td>
                    {% endif -%}
                </tr>
                {% endfor -%}
            </table>"""

msg = Template(table)
outputMSG = msg.render(names=names, ages=ages, length_list=len(names))
print(outputMSG)
