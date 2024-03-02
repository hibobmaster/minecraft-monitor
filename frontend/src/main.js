import 'mdui/mdui.css';
import 'mdui/components/layout.js';
import 'mdui/components/layout-item.js';
import 'mdui/components/layout-main.js';
import 'mdui/components/text-field.js';
import 'mdui/components/button.js';
import { prompt } from 'mdui/functions/prompt.js';
import { dialog } from 'mdui/functions/dialog.js';
import Chart from 'chart.js/auto';
import '@mdui/icons/copyright.js';


let ctx = document.getElementById("latency-chart").getContext('2d');
let chart = new Chart(
	ctx,
	{
		type: 'line',
		data: {
			labels: [], // 存储时间信息
			datasets: [{
				label: '延迟信息',
				data: [], // 存储延迟信息
				backgroundColor: 'rgba(0, 123, 255, 0.5)',
				borderColor: 'rgba(0, 123, 255, 1)',
				borderWidth: 1
			}]
		},
		options: {
			plugins: {
				title: {
					display: true,
					text: '延迟曲线图'
				},
				subtitle: {
					display: true,
					text: '单位: ms'
				}
			}
		}
	}
);

const restartBtn = document.getElementById("restart-server-btn")

window.onload = function () {
	fetch('http://127.0.0.1:10000/')
		.then(response => response.json())
		.then(data => {
			let compose_string = "";
			compose_string += "当前时间: " + data.time;
			compose_string += "\n服务器描述: " + data.description;
			compose_string += "\n延迟: " + data.latency + "ms";
			compose_string += "\n最大玩家容量: " + data.max;
			compose_string += "\n当前在线人数: " + data.online;
			document.getElementById("server-status").value = compose_string;

		})
		.catch(error => {
			console.log(error);
		});

	fetch('http://127.0.0.1:10000/get_latency')
		.then(response => response.json())
		.then(data => {
			for (let i = 0; i < data.length; i = i + 2) {
				chart.data.labels.push(data[i].time);
				chart.data.datasets[0].data.push(data[i].latency);
			}
			chart.update();
		});


	setInterval(function () {

		fetch('http://127.0.0.1:10000')
			.then(response => response.json())
			.then(data => {
				compose_string = "";
				compose_string += "当前时间: " + data.time;
				compose_string += "\n服务器描述: " + data.description;
				compose_string += "\n延迟: " + data.latency + "ms";
				compose_string += "\n最大玩家容量: " + data.max;
				compose_string += "\n当前在线人数: " + data.online;
				document.getElementById("server-status").value = compose_string;

				// 添加新的数据到图表并更新
				chart.data.labels.push(data.time);
				chart.data.datasets[0].data.push(data.latency);
				if (chart.data.labels.length > 30) {
					chart.data.labels.shift();
					chart.data.datasets[0].data.shift();
				}
				chart.update();
			});
	}, 30 * 1000);  // 每30s执行一次
};



restartBtn.addEventListener("click", () => {
	prompt({
		headline: "请输入重置密码",
		confirmText: "OK",
		cancelText: "Cancel",
		closeOnEsc: true,
		onConfirm: (value) => {
			restartBtn.disabled = true;
			restartBtn.loading = true;
			fetch("http://127.0.0.1:10000/restart-server", {
				method: "POST",
				headers: {
					"Accept": "application/json",
					"Content-Type": "application/json"
				},
				body: JSON.stringify({"code": value})
			})
			.then(response => response.json())
			.then(data => {
				dialog({
					headline: "执行结果",
					description: data.status,
					body: data.msg,
					actions: [
						{
							"text": "了解",
							onClick: () => {
								restartBtn.disabled = false;
								restartBtn.loading = false;
							}
						}
					]
				})
			});
		}
	});
});