package com.nsk.myProject.Services;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;

import com.nsk.myProject.Model.Order;
import com.nsk.myProject.Repositories.OrderRepository;

@Service
public class OrderService {
    private final OrderRepository orderRepository;
    public OrderService(OrderRepository orderRepository){
        this.orderRepository = orderRepository;
    }
    public Order createOrder(Order newOrder){
        orderRepository.save(newOrder);
        return newOrder;
    }
    public Optional<Order> getOrderById(Long id) {
        return orderRepository.findById(id);
    }

    public List<Order> getAllOrders() {
        return (List<Order>) orderRepository.findAll();
    }
}

