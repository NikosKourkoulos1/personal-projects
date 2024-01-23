package com.nsk.myProject.Repositories;

import org.springframework.data.repository.CrudRepository;

import com.nsk.myProject.Model.Order;

public interface OrderRepository extends CrudRepository <Order, Long>{
    
}
