import { Component, OnInit, ViewChild } from '@angular/core';
import { TransactionsService } from './transactions.service';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import { TransactionDialogComponent } from './transaction-dialog/transaction-dialog.component';
import {MatDialog, MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'app-transactions',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.css']
})
export class TransactionsComponent implements OnInit {
  title = 'Transactions';

  constructor(
    private transactionService: TransactionsService,
    private dialog: MatDialog
  ) { }

  transactionDialog: MatDialogRef<TransactionDialogComponent>;

  transactionData: any = [];
  columnsToDisplay = ['date', 'description', 'transactionType', 'transactionAmount'];
  dataSource: any;

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
  @ViewChild(MatSort, {static: true}) sort: MatSort;

  ngOnInit(): void {
    this.transactionService.getTransactions().subscribe((data) => {
      this.transactionData = data
      // setup table
      this.dataSource = new MatTableDataSource(this.transactionData);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
  }

  searchFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  typeFilter(event: Event) {
    this.dataSource.filter = event;
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  openTransaction(data) {
    this.transactionDialog = this.dialog.open(TransactionDialogComponent, {
      data: {
        transaction: data
      },
      autoFocus: false
    });
  }

}
