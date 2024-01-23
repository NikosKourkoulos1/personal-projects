package com.nsk.myProject.Model;

import java.time.LocalDate;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "orders")
public class Order {
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, name = "id")
    private long id;
    
    @Column(nullable = false, name = "name")
    private String name;
    
    @Column(nullable = false, name = "date")
    private LocalDate  date;
    
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "customer_id", nullable = false)
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler", "orders", "email"})
    private Customer customer;

   public Long getId() {
      return id;
   }
   
   public void setId(Long id) {
      this.id = id;
   }
   
   public String getName() {
      return name;
   }
   
   public void setName(String name) {
      this.name = name;
   }

   public void setDate(LocalDate date){
      this.date = date;
   }
     
   public LocalDate getDate(){
      return date;
   }

   public Customer getCustomer() {
      return customer;
   } 

   public void setCustomer(Customer customer) {
      this.customer = customer;
   }

   public Order orElseThrow(Object object) {
      throw new UnsupportedOperationException("Unimplemented method 'orElseThrow'");
   }
}




