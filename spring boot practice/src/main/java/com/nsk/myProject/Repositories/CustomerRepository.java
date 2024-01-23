package com.nsk.myProject.Repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import com.nsk.myProject.Model.Customer;

public interface CustomerRepository extends JpaRepository<Customer, Long> {
}
