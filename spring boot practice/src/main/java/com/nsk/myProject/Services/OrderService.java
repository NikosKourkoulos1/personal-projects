package com.nsk.myProject.Services;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.nsk.myProject.Model.Customer;
import com.nsk.myProject.Model.Order;
import com.nsk.myProject.Repositories.CustomerRepository;
import com.nsk.myProject.Repositories.OrderRepository;

@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final CustomerRepository customerRepository;

    @Autowired
    public OrderService(OrderRepository orderRepository, CustomerRepository customerRepository) {
        this.orderRepository = orderRepository;
        this.customerRepository = customerRepository;
    }

    public Order createOrder(Order newOrder, Long customerId) {
        // Find the customer based on customerId
        Customer customer = customerRepository.findById(customerId)
                            .orElseThrow(() -> new RuntimeException("Customer not found with ID: " + customerId));

        // Associate the customer with the new order
        newOrder.setCustomer(customer);

        // Save the new order
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
