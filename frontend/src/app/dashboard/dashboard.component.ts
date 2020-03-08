import { Component, OnInit } from '@angular/core';
import { DashboardService } from './dashboard.service';
import { ChartType, ChartOptions } from 'chart.js';
import { Label } from 'ng2-charts';
import * as pluginDataLabels from 'chartjs-plugin-datalabels';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  title = 'Dashboard';

  constructor(private service: DashboardService) { }

  months = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  loading: boolean = true;
  data: any;
  date: Date = new Date();

  earnings = [];
  spending = [];
  monthlySpendTotal: number;
  monthlyEarnTotal: number;
  yearlySpendTotal: number;
  yearlyEarnTotal: number;

  public pieChartOptions: ChartOptions = {
    responsive: true,
    legend: {
      position: 'top',
    },
    plugins: {
      datalabels: {
        formatter: (value, ctx) => {
          const label = ctx.chart.data.labels[ctx.dataIndex];
          return label;
        },
      },
    }
  };
  public pieChartPlugins = [pluginDataLabels];
  public pieChartColors = [
    {
      backgroundColor: ['rgb(240,128,128)', 'rgb(144,238,144)'],
    },
  ];

  public pieChartLabels: Label[] = ['Spent', 'Earned'];
  public yearlyPieChartData: number[] = []
  public monthlyPieChartData: number[] = []

  ngOnInit(): void {
    this.service.getTransactions().subscribe((data) => {
      this.data = data;
      this.earnings = this.data.filter((element) => {
        return element.transactionType == 'Credit';
      });
      this.spending = this.data.filter((element) => {
        return element.transactionType == 'Debit' || element.transactionType == 'Authorisation';
      });
      this.monthlyStats();
      this.yearlyStats();
      this.loading = false;
    });
  }

  monthlyStats() {
    let month = this.date.getMonth();
    let year = this.date.getFullYear();
    let start = new Date(year, month, 0, 1, 0, 0, 0);
    let end = new Date(year, month + 1, 0, 0, 0, 0);

    // spend
    let monthlySpend = this.spending.filter((element) => {
      let date = new Date(element.date);
      return date >= start && date <= end;
    });
    let monthlySpendTotal = monthlySpend.reduce((total, current) => {
      return total + current.transactionAmount;
    }, 0);

    // earn
    let monthlyEarn = this.earnings.filter((element) => {
      let date = new Date(element.date);
      return date >= start && date <= end;
    });
    let monthlyEarnTotal = monthlyEarn.reduce((total, current) => {
      return total + current.transactionAmount;
    }, 0);

    this.monthlySpendTotal = monthlySpendTotal.toFixed(2);
    this.monthlyEarnTotal = monthlyEarnTotal.toFixed(2);
    this.monthlyPieChartData = [this.monthlySpendTotal, this.monthlyEarnTotal];
  }

  yearlyStats() {
    let year = this.date.getFullYear()
    let month = this.date.getMonth()
    let start = new Date(year, 0, 1, 0, 0, 0, 0);
    let end = new Date(year, month + 1, 0, 23, 59, 59, 59);

    // spend
    let yearlySpend = this.spending.filter((element) => {
      let date = new Date(element.date);
      return date >= start && date <= end;
    });
    let yearlySpendTotal = yearlySpend.reduce((total, current) => {
      return total + current.transactionAmount;
    }, 0);

    // earn
    let yearlyEarn = this.earnings.filter((element) => {
      let date = new Date(element.date);
      return date >= start && date <= end;
    });
    let yearlyEarnTotal = yearlyEarn.reduce((total, current) => {
      return total + current.transactionAmount;
    }, 0);

    this.yearlySpendTotal = yearlySpendTotal.toFixed(2);
    this.yearlyEarnTotal = yearlyEarnTotal.toFixed(2);
    this.yearlyPieChartData = [this.yearlySpendTotal, this.yearlyEarnTotal];
  }

  changeMonth(increment) {
    this.date = new Date(this.date.setMonth(this.date.getMonth() + increment));
    this.yearlyStats();
    this.monthlyStats();
  }

  resetDate() {
    this.date = new Date()
    this.yearlyStats();
    this.monthlyStats();
  }
}
